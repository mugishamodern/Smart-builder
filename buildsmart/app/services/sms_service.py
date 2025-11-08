"""
SMS service for sending SMS notifications.

This module provides functionality for sending SMS notifications
using Twilio or Africa's Talking API.
"""
from flask import current_app
import os


class SMSService:
    """Service for sending SMS notifications"""
    
    # Provider types
    TWILIO = 'twilio'
    AFRICAS_TALKING = 'africas_talking'
    
    @staticmethod
    def send_sms(phone_number, message):
        """
        Send SMS message.
        
        Args:
            phone_number: Phone number (with country code)
            message: Message content
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        provider = current_app.config.get('SMS_PROVIDER', 'twilio').lower()
        
        if provider == SMSService.TWILIO:
            return SMSService._send_via_twilio(phone_number, message)
        elif provider == SMSService.AFRICAS_TALKING:
            return SMSService._send_via_africas_talking(phone_number, message)
        else:
            current_app.logger.warning(f'Unknown SMS provider: {provider}')
            return False
    
    @staticmethod
    def _send_via_twilio(phone_number, message):
        """
        Send SMS via Twilio.
        
        Args:
            phone_number: Phone number
            message: Message content
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            from twilio.rest import Client
            
            account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
            auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
            from_number = current_app.config.get('TWILIO_FROM_NUMBER')
            
            if not all([account_sid, auth_token, from_number]):
                current_app.logger.warning('Twilio credentials not configured')
                return False
            
            client = Client(account_sid, auth_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=from_number,
                to=phone_number
            )
            
            current_app.logger.info(f'SMS sent via Twilio: {message_obj.sid}')
            return True
            
        except ImportError:
            current_app.logger.warning('Twilio library not installed. Install with: pip install twilio')
            return False
        except Exception as e:
            current_app.logger.error(f'Error sending SMS via Twilio: {str(e)}')
            return False
    
    @staticmethod
    def _send_via_africas_talking(phone_number, message):
        """
        Send SMS via Africa's Talking.
        
        Args:
            phone_number: Phone number
            message: Message content
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            from africastalking.AfricasTalkingGateway import AfricasTalkingGateway
            
            username = current_app.config.get('AT_USERNAME')
            api_key = current_app.config.get('AT_API_KEY')
            sender_id = current_app.config.get('AT_SENDER_ID', 'BUILDSMART')
            
            if not all([username, api_key]):
                current_app.logger.warning('Africa\'s Talking credentials not configured')
                return False
            
            gateway = AfricasTalkingGateway(username, api_key)
            
            recipients = [phone_number]
            result = gateway.sendMessage(recipients, message, sender_id)
            
            if result and result['status'] == 'Success':
                current_app.logger.info(f'SMS sent via Africa\'s Talking: {phone_number}')
                return True
            else:
                current_app.logger.error(f'Failed to send SMS via Africa\'s Talking: {result}')
                return False
                
        except ImportError:
            current_app.logger.warning('Africa\'s Talking library not installed. Install with: pip install africastalking')
            return False
        except Exception as e:
            current_app.logger.error(f'Error sending SMS via Africa\'s Talking: {str(e)}')
            return False
    
    @staticmethod
    def send_notification(phone_number, title, message):
        """
        Send notification SMS.
        
        Args:
            phone_number: Phone number
            title: Notification title
            message: Notification message
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        full_message = f"{title}\n\n{message}"
        return SMSService.send_sms(phone_number, full_message)
    
    @staticmethod
    def send_verification_code(phone_number, code):
        """
        Send verification code SMS.
        
        Args:
            phone_number: Phone number
            code: Verification code
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        message = f"Your BuildSmart verification code is: {code}. Valid for 10 minutes."
        return SMSService.send_sms(phone_number, message)
    
    @staticmethod
    def send_order_update(phone_number, order_number, status):
        """
        Send order update SMS.
        
        Args:
            phone_number: Phone number
            order_number: Order number
            status: Order status
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        message = f"Your order {order_number} status has been updated to {status}."
        return SMSService.send_sms(phone_number, message)

