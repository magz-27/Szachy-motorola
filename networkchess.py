import time
import threading
import socket
import json
import select


def getBoardFromCoord(board, coord):
    if coord[0] > 7 or coord[0] < 0 or coord[1] > 7 or coord[1] < 0:
        return None
    index = coord[0] + coord[1] * 8
    return board[index]


class ChessNetworkGame:
    
    def __init__(self, is_host=False, host='localhost', port=5000):
        self.is_host = is_host
        self.host = host
        self.port = port
        self.socket = None
        self.connection = None
        self.connected = False
        self.opponent_address = None
        
        # Network statistics
        self.ping = 0
        self.last_response_time = 0
        self.packet_count = 0
        self.last_ping_time = time.time()
        self.connection_time = time.time()
        
        # Game state
        self.move_queue = []
        self.undo_requested = False
        self.suggestion_enabled = False
        
        # Thread control
        self.keep_running = True
        self.connection_active = False
        
        # Zabezpieczenie współdzielonych zmiennych
        self.lock = threading.Lock()
        
    def start_connection(self):
        """Begins the connection process manually"""
        # Upewnij się, że nie mamy już aktywnego wątku
        if hasattr(self, 'connection_thread') and self.connection_thread.is_alive():
            print("Connection thread already running")
            return
            
        # Utwórz i uruchom wątek
        self.connection_thread = threading.Thread(target=self._establish_connection)
        self.connection_thread.daemon = True
        self.connection_thread.start()
        
    def _establish_connection(self):
        """Establish connection in a background thread"""
        try:
            print("Starting connection establishment...")
            # Upewnij się, że nie próbujemy nawiązać połączenia, jeśli już jest aktywne
            with self.lock:
                if self.connection_active:
                    print("Connection already active, skipping")
                    return
                print("Setting connection_active to True")
                self.connection_active = True
            
            if self.is_host:
                print("Setting up as host...")
                self.setup_host()
            else:
                print("Setting up as client...")
                self.setup_client()
            
            # Rozpocznij ping monitoring tylko jeśli połączenie jest aktywne
            with self.lock:
                if self.connected:
                    print("Starting ping monitoring thread...")
                    self.ping_thread = threading.Thread(target=self._monitor_ping)
                    self.ping_thread.daemon = True
                    self.ping_thread.start()
                    print("### CONNECTION SUCCESSFUL ###")
                else:
                    print("Not connected, not starting ping thread")
            
        except Exception as e:
            print(f"Connection error: {e}")
            with self.lock:
                self.connected = False
                self.connection_active = False
    
    def setup_host(self):
        """Configure server (host)"""
        try:
            # Zamknij istniejące połączenia i sockety
            print("Closing existing connections...")
            self._close_existing_connections()
            
            print("Creating new socket...")
            # Utwórz nowy socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"New socket created: {self.socket}")
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Ustaw timeout dla operacji akceptowania połączenia
            self.socket.settimeout(30)  # 30-sekundowy timeout
            
            # Bindowanie portu i adresu
            try:
                print(f"Binding to {self.host}:{self.port}...")
                self.socket.bind((self.host, self.port))
            except socket.error as e:
                print(f"Binding error: {e}")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
                return
                
            # Nasłuchiwanie połączeń
            self.socket.listen(1)
            print("### WAITING FOR CONNECTION... DO NOT PANIC IF IT LOOKS STUCK ###")
            
            # Akceptowanie połączenia
            try:
                self.connection, self.opponent_address = self.socket.accept()
                print(f"Connection accepted: {self.connection}")
                with self.lock:
                    self.connected = True
                    self.connection_time = time.time()
                print(f"Connected to {self.opponent_address}")
            except socket.timeout:
                print("Connection timeout - no clients connected")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
            
        except Exception as e:
            print(f"Host setup error: {e}")
            with self.lock:
                self.connected = False
                self.connection_active = False
            
    def setup_client(self):
        """Configure client"""
        try:
            # Zamknij istniejące połączenia i sockety
            print("Closing existing connections (client mode)...")
            self._close_existing_connections()
            
            # Utwórz nowy socket
            print("Creating new client socket...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"New client socket created: {self.socket}")
            self.socket.settimeout(10)  # 10-sekundowy timeout dla połączenia
            
            print(f"Connecting to {self.host}:{self.port}...")
            
            # Próba połączenia
            try:
                self.socket.connect((self.host, self.port))
                self.socket.settimeout(None)  # Reset timeout po połączeniu
                self.connection = self.socket
                self.opponent_address = (self.host, self.port)
                with self.lock:
                    self.connected = True
                    self.connection_time = time.time()
                print("Connected to server")
            except socket.timeout:
                print("Connection timeout - could not connect to server")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
            except socket.error as e:
                print(f"Connection error: {e}")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
                
        except Exception as e:
            print(f"Client setup error: {e}")
            with self.lock:
                self.connected = False
                self.connection_active = False
    
    def _close_existing_connections(self):
        """Close any existing socket and connection"""
        # Zamknij istniejące połączenie
        if self.connection:
            try:
                self.connection.close()
                print("Existing connection closed")
            except Exception as e:
                print(f"Error closing connection: {e}")
            self.connection = None
            
        # Zamknij istniejący socket
        if self.socket:
            try:
                self.socket.close()
                print("Existing socket closed")
            except Exception as e:
                print(f"Error closing socket: {e}")
            self.socket = None
    
    def _monitor_ping(self):
        """Monitor connection ping in a separate thread"""
        last_pong_time = time.time()
        
        while self.keep_running:
            try:
                with self.lock:
                    if not self.connected:
                        time.sleep(1)
                        continue
                
                # Sprawdź, czy nie otrzymaliśmy PONG przez 15 sekund
                current_time = time.time()
                if current_time - last_pong_time > 15:
                    print("Connection timeout - no PONG received")
                    with self.lock:
                        self.connected = False
                        self.connection_active = False
                    break
                
                # Wyślij ping co 5 sekund
                if current_time - self.last_ping_time > 5:
                    if self.send_message('PING'):
                        self.last_ping_time = time.time()
                    else:
                        # Jeśli wysłanie wiadomości nie powiodło się, zakończ wątek
                        with self.lock:
                            self.connected = False
                            self.connection_active = False
                        break
                    
                # Gdy otrzymamy PONG, zaktualizujemy last_pong_time
                if current_time - self.last_ping_time < 2:  # Jeśli niedawno otrzymaliśmy odpowiedź
                    last_pong_time = current_time
                    
                time.sleep(1)
            except Exception as e:
                print(f"Ping monitoring error: {e}")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
                break
    
    def send_message(self, message):
        """Send a message to opponent"""
        try:
            with self.lock:
                if not self.connected or not self.connection:
                    print("Cannot send message: not connected")
                    return False
                    
            # Sprawdź, czy połączenie jest ważne
            if not isinstance(self.connection, socket.socket):
                print(f"Invalid connection object: {type(self.connection)}")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
                return False
                    
            if isinstance(message, str):
                self.connection.send(message.encode())
            else:
                self.connection.send(message)
            return True
        except (socket.error, ConnectionResetError) as e:
            print(f"Socket error while sending message: {e}")
            with self.lock:
                self.connected = False
                self.connection_active = False
            return False
        except Exception as e:
            print(f"Send message error: {e}")
            with self.lock:
                self.connected = False
                self.connection_active = False
            return False
    
    def serialize_move(self, start_square, end_square):
        """Serialize a move to send"""
        return json.dumps({
            'type': 'MOVE',
            'start_coord': start_square.coord,
            'end_coord': end_square.coord,
            'timestamp': time.time()
        })
    
    def deserialize_move(self, move_data):
        """Deserialize a move from json string"""
        try:
            move_dict = json.loads(move_data)
            if move_dict.get('type') == 'MOVE':
                return move_dict['start_coord'], move_dict['end_coord']
            return None  # Explicit return None for non-MOVE types
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error deserializing move: {e}")
            return None
        
    def send_move(self, start_square, end_square):
        """Send a move to opponent"""
        move_data = self.serialize_move(start_square, end_square)
        return self.send_message(move_data)
    
    def send_undo_request(self):
        """Send undo request"""
        self.undo_requested = True
        return self.send_message(json.dumps({'type': 'UNDO_REQUEST'}))
    
    def send_undo_response(self, accepted):
        """Send response to undo request"""
        response = json.dumps({
            'type': 'UNDO_RESPONSE',
            'accepted': accepted
        })
        return self.send_message(response)
    
    def toggle_suggestions(self, enabled):
        """Toggle move suggestions"""
        self.suggestion_enabled = enabled
        message = json.dumps({
            'type': 'SUGGESTION_TOGGLE',
            'enabled': enabled
        })
        return self.send_message(message)

    def handle_network_events(self, board):
        """Handle incoming network events"""
        try:
            with self.lock:
                if not self.connected or not self.connection:
                    return None
            
            # Sprawdź, czy połączenie jest ważne
            if not isinstance(self.connection, socket.socket):
                print(f"Invalid connection object in handle_network_events: {type(self.connection)}")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
                return "CONNECTION_LOST"
                    
            # Sprawdź, czy dane są dostępne do odczytu
            try:
                ready = select.select([self.connection], [], [], 0.01)
                if not ready[0]:
                    return None
            except (socket.error, ValueError) as e:
                print(f"Socket select error: {e}")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
                return "CONNECTION_LOST"
                    
            try:
                data = self.connection.recv(1024)
                if not data:
                    print("Connection lost - no data received")
                    with self.lock:
                        self.connected = False
                        self.connection_active = False
                    return "CONNECTION_LOST"
            except (socket.error, ConnectionResetError) as e:
                print(f"Socket receive error: {e}")
                with self.lock:
                    self.connected = False
                    self.connection_active = False
                return "CONNECTION_LOST"
                    
            try:
                message = data.decode()
            except UnicodeDecodeError:
                print("Message decoding error")
                return None
                
            # Handle ping messages
            if message == 'PING':
                self.send_message('PONG')
                return None
            elif message == 'PONG':
                with self.lock:
                    self.ping = int((time.time() - self.last_ping_time) * 1000)  # milliseconds
                return None
            
            # Handle JSON messages
            try:
                try:
                    parsed = json.loads(message)
                    message_type = parsed.get('type', '')
                except json.JSONDecodeError:
                    return message
                
                if message_type == 'MOVE':
                    start_coord = parsed['start_coord']
                    end_coord = parsed['end_coord']

                    start_square = getBoardFromCoord(board, start_coord)
                    end_square = getBoardFromCoord(board, end_coord)
                    
                    if start_square is None or end_square is None:
                        print(f"Error: Could not find squares {start_coord} or {end_coord}")
                        return None
                        
                    with self.lock:
                        self.last_response_time = time.time() - parsed.get('timestamp', time.time())
                        self.packet_count += 1
                    return start_square, end_square
                    
                elif message_type == 'UNDO_REQUEST':
                    return 'UNDO_REQUEST'

                elif message_type == 'UNDO_RESPONSE':
                    if parsed['accepted']:
                        return 'UNDO_ACCEPTED'
                    else:
                        return 'UNDO_REJECTED'

                elif message_type == "RESET":
                    return "RESET"

                elif message_type == 'SUGGESTION_TOGGLE':
                    with self.lock:
                        self.suggestion_enabled = parsed['enabled']
                    return f"SUGGESTION_{'ENABLED' if self.suggestion_enabled else 'DISABLED'}"
                
                return None  # Unknown message type
            except Exception as e:
                print(f"Error processing message: {e}")
                return None
                    
        except ConnectionResetError:
            print("Connection reset by peer")
            with self.lock:
                self.connected = False
                self.connection_active = False
            return "CONNECTION_LOST"
        except Exception as e:
            print(f"Error handling network events: {e}")
            with self.lock:
                self.connected = False
                self.connection_active = False
            return "CONNECTION_LOST"
    
    def get_network_stats(self):
        """Get network statistics for nerd view"""
        with self.lock:
            return {
                'connected': self.connected,
                'opponent_address': self.opponent_address,
                'ping': f"{self.ping} ms",
                'connection_time': time.time() - self.connection_time,
                'response_time': f"{self.last_response_time*1000:.2f} ms",
                'packet_count': self.packet_count,
                'is_host': self.is_host
            }
    
    def close_connection(self):
        """Close the connection"""
        self.keep_running = False  # Stop threads
        
        with self.lock:
            self.connected = False
            self.connection_active = False
            
        self._close_existing_connections()
        
    def reconnect(self):
        """Attempt to reconnect"""
        # Upewnij się, że stare połączenia są zamknięte
        self.close_connection()
        
        # Resetuj zmienne
        with self.lock:
            self.connected = False
            self.connection_active = False
            self.keep_running = True
            
        # Uruchom nowy wątek połączenia
        self.start_connection()