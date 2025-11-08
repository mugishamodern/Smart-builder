import 'dart:async';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:buildsmart_mobile/core/config/app_config.dart';

/// SocketService for managing WebSocket connections
/// 
/// Handles connection, disconnection, and event listening for real-time messaging
class SocketService {
  SocketService._();
  
  static SocketService? _instance;
  static SocketService get instance {
    _instance ??= SocketService._();
    return _instance!;
  }
  
  IO.Socket? _socket;
  bool _isConnected = false;
  final _connectionController = StreamController<bool>.broadcast();
  final _messageController = StreamController<Map<String, dynamic>>.broadcast();
  
  /// Connection status stream
  Stream<bool> get connectionStream => _connectionController.stream;
  
  /// Message stream for receiving new messages
  Stream<Map<String, dynamic>> get messageStream => _messageController.stream;
  
  /// Check if socket is connected
  bool get isConnected => _isConnected && _socket?.connected == true;
  
  /// Connect to SocketIO server
  /// 
  /// [userId] - Current user ID for authentication
  Future<void> connect({required int userId}) async {
    if (_socket != null && _isConnected) {
      return; // Already connected
    }
    
    try {
      final baseUrl = AppConfig.instance.apiBaseUrl;
      
      _socket = IO.io(
        baseUrl,
        IO.OptionBuilder()
          .setTransports(['websocket'])
          .enableAutoConnect()
          .setExtraHeaders({'user_id': userId.toString()})
          .build(),
      );
      
      // Connection event handlers
      _socket!.onConnect((_) {
        _isConnected = true;
        _connectionController.add(true);
        print('Socket connected');
      });
      
      _socket!.onDisconnect((_) {
        _isConnected = false;
        _connectionController.add(false);
        print('Socket disconnected');
      });
      
      _socket!.onError((error) {
        print('Socket error: $error');
        _isConnected = false;
        _connectionController.add(false);
      });
      
      // Message event handlers
      _socket!.on('new_message', (data) {
        if (data is Map) {
          _messageController.add(Map<String, dynamic>.from(data));
        }
      });
      
      _socket!.on('typing', (data) {
        // Handle typing indicator
        print('Typing event: $data');
      });
      
      _socket!.on('message_read', (data) {
        // Handle message read confirmation
        print('Message read: $data');
      });
      
      _socket!.connect();
    } catch (e) {
      print('Error connecting to socket: $e');
      _isConnected = false;
      _connectionController.add(false);
    }
  }
  
  /// Disconnect from SocketIO server
  Future<void> disconnect() async {
    if (_socket != null) {
      _socket!.disconnect();
      _socket!.dispose();
      _socket = null;
      _isConnected = false;
      _connectionController.add(false);
    }
  }
  
  /// Join a conversation room
  void joinConversation({required int userId, required int otherUserId}) {
    if (!isConnected) return;
    
    _socket!.emit('join_conversation', {
      'user_id': userId,
      'other_user_id': otherUserId,
    });
  }
  
  /// Send a typing indicator
  void sendTyping({required int receiverId, required bool isTyping}) {
    if (!isConnected) return;
    
    _socket!.emit('typing', {
      'receiver_id': receiverId,
      'is_typing': isTyping,
    });
  }
  
  /// Mark message as read
  void markAsRead({required int messageId}) {
    if (!isConnected) return;
    
    _socket!.emit('mark_as_read', {
      'message_id': messageId,
    });
  }
  
  /// Dispose resources
  void dispose() {
    disconnect();
    _connectionController.close();
    _messageController.close();
  }
}
