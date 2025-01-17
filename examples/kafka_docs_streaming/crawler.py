@@ -11,6 +11,9 @@ import logging
 
 # Configure logging
 # Constants
+RETRY_DELAY_SECONDS = 60
+
 logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
@@ -112,7 +115,7 @@ class DocsCrawler:
             except Exception as e:
                 logger.error(f"Error in crawler loop: {str(e)}")
                 # Wait before retrying
-                time.sleep(60)
+                time.sleep(RETRY_DELAY_SECONDS)