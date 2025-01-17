import os
import yaml
import json
from kafka import KafkaConsumer
import logging
import tkinter as tk
from tkinter import ttk
import webbrowser
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocsViewer:
    def __init__(self):
        # Load configuration
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize Kafka consumer
        self.consumer = KafkaConsumer(
            self.config['kafka']['topic'],
            bootstrap_servers=self.config['kafka']['bootstrap_servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='docs_viewer_group'
        )
        
        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Kafka Documentation Viewer")
        self.root.geometry("800x600")

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create treeview for documentation list
        self.tree = ttk.Treeview(main_frame, columns=('Title', 'URL', 'Last Updated'), show='headings')
        self.tree.heading('Title', text='Title')
        self.tree.heading('URL', text='URL')
        self.tree.heading('Last Updated', text='Last Updated')
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind double-click event
        self.tree.bind('<Double-1>', self.open_url)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def open_url(self, event):
        """Open URL in default browser when item is double-clicked"""
        selected_item = self.tree.selection()[0]
        url = self.tree.item(selected_item)['values'][1]
        webbrowser.open(url)

    def update_gui(self, message):
        """Update GUI with new documentation"""
        try:
            # Format timestamp
            timestamp = datetime.fromisoformat(message['timestamp'])
            formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert new item
            self.tree.insert(
                '',
                'end',
                values=(
                    message.get('title', 'No title'),
                    message['url'],
                    formatted_time
                )
            )
        except Exception as e:
            logger.error(f"Error updating GUI: {str(e)}")

    def run(self):
        """Main viewer loop"""
        logger.info("Starting documentation viewer...")
        
        def check_messages():
            """Check for new Kafka messages"""
            try:
                # Non-blocking check for messages
                for message in self.consumer.poll(timeout_ms=100).values():
                    for record in message:
                        self.update_gui(record.value)
            except Exception as e:
                logger.error(f"Error checking messages: {str(e)}")
            
            # Schedule next check
            self.root.after(1000, check_messages)

        # Start checking messages
        check_messages()
        
        # Start GUI main loop
        self.root.mainloop()

if __name__ == "__main__":
    viewer = DocsViewer()
    viewer.run()