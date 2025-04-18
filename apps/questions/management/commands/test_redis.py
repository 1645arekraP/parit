from django.core.management.base import BaseCommand
import os
import redis
import time

class Command(BaseCommand):
    help = 'Test Redis connection and diagnose issues'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting Redis connection test..."))
        
        # Build Redis URL from environment variables
        redis_url = f"redis://{os.getenv('REDIS_USERNAME')}:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_CHANNEL_DB')}"
        
        self.stdout.write(f"Testing connection to: redis://user:***@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_CHANNEL_DB')}")
        
        try:
            # Test regular connection
            r = redis.Redis.from_url(redis_url)
            
            # Test ping
            start = time.time()
            ping_result = r.ping()
            end = time.time()
            ping_time = round((end - start) * 1000, 2)
            
            self.stdout.write(self.style.SUCCESS(f"PING successful (took {ping_time}ms)"))
            
            # Test basic operations
            r.set('test_key', 'test_value')
            value = r.get('test_key')
            if value == b'test_value':
                self.stdout.write(self.style.SUCCESS("SET/GET operations successful"))
            else:
                self.stdout.write(self.style.ERROR(f"SET/GET test failed. Got: {value}"))
            
            # Clean up
            r.delete('test_key')
            
            # Get server info
            info = r.info()
            self.stdout.write("\nRedis Server Info:")
            self.stdout.write(f"  Redis Version: {info.get('redis_version')}")
            self.stdout.write(f"  Connected Clients: {info.get('connected_clients')}")
            self.stdout.write(f"  Used Memory: {info.get('used_memory_human')}")
            
            # Test connection stability
            self.stdout.write("\nTesting connection stability...")
            for i in range(3):
                r.set(f'stability_test_{i}', f'value_{i}')
                time.sleep(0.5)
                value = r.get(f'stability_test_{i}')
                self.stdout.write(f"  Iteration {i+1}: {'✓' if value == f'value_{i}'.encode() else '✗'}")
                r.delete(f'stability_test_{i}')
            
            self.stdout.write(self.style.SUCCESS("\nAll Redis tests completed successfully!"))
            
        except redis.exceptions.ConnectionError as e:
            self.stdout.write(self.style.ERROR(f"Connection Error: {e}"))
            self.stdout.write(self.style.WARNING("This indicates your application cannot reach the Redis server."))
            self.stdout.write("Possible causes:")
            self.stdout.write("- Incorrect connection details")
            self.stdout.write("- Network/firewall issues")
            self.stdout.write("- Redis server is down")
            self.stdout.write("- Authentication failure")
        except redis.exceptions.TimeoutError as e:
            self.stdout.write(self.style.ERROR(f"Timeout Error: {e}"))
            self.stdout.write(self.style.WARNING("This suggests network latency or an overloaded Redis server."))
        except redis.exceptions.AuthenticationError as e:
            self.stdout.write(self.style.ERROR(f"Authentication Error: {e}"))
            self.stdout.write(self.style.WARNING("Check your Redis username and password."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {type(e).__name__}: {e}"))