import time
import threading
import socket
import json
import select


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
        
        # Start connection in a separate thread to avoid blocking the UI
        self.connection_thread = threading.Thread(target=self._establish_connection)
        self.connection_thread.daemon = True
        self.connection_thread.start()
    def setup_client(self):
   
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout for connection
            print(f"Łączenie z {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(None)  # Reset timeout po połączeniu
            self.connection = self.socket
            self.opponent_address = (self.host, self.port)
            self.connected = True
            self.connection_time = time.time()
            print("Connected to server")
        except Exception as e:
            print(f"Client setup error: {e}")
            self.connected = False
    def _establish_connection(self):
        """Establish connection in a background thread"""
        try:
            if self.is_host:
                self.setup_host()
            else:
                self.setup_client()
            
            # Start ping monitoring thread
            self.ping_thread = threading.Thread(target=self._monitor_ping)
            self.ping_thread.daemon = True
            self.ping_thread.start()
            
        except Exception as e:
            print(f"Connection error: {e}")
            self.connected = False
    
    def setup_host(self):
        """Configure server (host)"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            print("Waiting for connection...")
            self.connection, self.opponent_address = self.socket.accept()
            self.connected = True
            self.connection_time = time.time()
            print(f"Connected to {self.opponent_address}")
        except Exception as e:
            print(f"Host setup error: {e}")
            self.connected = False
        
    def setup_client(self):
        """Configure client"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout for connection
            self.socket.connect((self.host, self.port))
            self.connection = self.socket
            self.opponent_address = (self.host, self.port)
            self.connected = True
            self.connection_time = time.time()
            print("Connected to server")
        except Exception as e:
            print(f"Client setup error: {e}")
            self.connected = False
    
    def _monitor_ping(self):
        """Monitor connection ping in a separate thread"""
        while self.connected:
            try:
                # Send ping request every 5 seconds
                if time.time() - self.last_ping_time > 5:
                    ping_start = time.time()
                    self.send_message('PING')
                    self.last_ping_time = time.time()
                    
                time.sleep(1)
            except Exception as e:
                print(f"Ping monitoring error: {e}")
    
    def send_message(self, message):
        """Send a message to opponent"""
        try:
            if not self.connected:
                return False
                
            if isinstance(message, str):
                self.connection.send(message.encode())
            else:
                self.connection.send(message)
            return True
        except Exception as e:
            print(f"Send message error: {e}")
            self.connected = False
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
    
        try:
            move_dict = json.loads(move_data)
            if move_dict.get('type') == 'MOVE':
                return move_dict['start_coord'], move_dict['end_coord']
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
    
        try:
            if not self.connected:
                return None
                    
            # Check if data is available to read
            ready = select.select([self.connection], [], [], 0.01)
            if not ready[0]:
                return None
                    
            data = self.connection.recv(1024)
            if not data:
                print("Połączenie utracone - brak danych")
                self.connected = False
                return "CONNECTION_LOST"
                    
            try:
                message = data.decode()
            except UnicodeDecodeError:
                print("Błąd dekodowania wiadomości")
                return None
                
            # Handle ping messages
            if message == 'PING':
                self.send_message('PONG')
                return None
            elif message == 'PONG':
                self.ping = int((time.time() - self.last_ping_time) * 1000)  # milliseconds
                return None
            
            # Handle JSON messages
            try:
                from main import getBoardFromCoord
                parsed = json.loads(message)
                message_type = parsed.get('type', '')
                
                if message_type == 'MOVE':
                    start_coord = parsed['start_coord']
                    end_coord = parsed['end_coord']
                    start_square = getBoardFromCoord(board, start_coord)
                    end_square = getBoardFromCoord(board, end_coord)
                    if start_square is None or end_square is None:
                        print(f"Błąd: nie można znaleźć pól {start_coord} lub {end_coord}")
                        return None
                    self.last_response_time = time.time() - parsed.get('timestamp', time.time())
                    self.packet_count += 1
                    return (start_square, end_square)
                    
                elif message_type == 'UNDO_REQUEST':
                    return 'UNDO_REQUEST'
                    
                elif message_type == 'UNDO_RESPONSE':
                    if parsed['accepted']:
                        return 'UNDO_ACCEPTED'
                    else:
                        return 'UNDO_REJECTED'
                        
                elif message_type == 'SUGGESTION_TOGGLE':
                    self.suggestion_enabled = parsed['enabled']
                    return f"SUGGESTION_{'ENABLED' if self.suggestion_enabled else 'DISABLED'}"
            except json.JSONDecodeError:
                # Not a JSON message
                print(f"Otrzymano nieprawidłowy format JSON: {message}")
            except Exception as e:
                print(f"Błąd przetwarzania wiadomości: {e}")
                    
        except ConnectionResetError:
            print("Połączenie zresetowane przez drugą stronę")
            self.connected = False
            return "CONNECTION_LOST"
        except Exception as e:
            print(f"Error handling network events: {e}")
            if "Connection" in str(e):
                self.connected = False
                return "CONNECTION_LOST"
            return None
    
    def get_network_stats(self):
        """Get network statistics for nerd view"""
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
        self.connected = False
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
        if self.socket:
            try:
                self.socket.close()
            except:
                pass