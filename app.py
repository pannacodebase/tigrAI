from flask import Flask, request, jsonify, render_template, Response
import time  # Import time module to use time.sleep()

app = Flask(__name__)

# Store all messages (instead of just the latest one)
messages = [{"response": ""}]
subscribers = []

@app.route('/')
def index():
    # Pass the history of messages to the frontend
    return render_template('index.html', messages=messages)

@app.route('/echo', methods=['POST'])
def echo():
    global messages
    data = request.get_json()
    new_message = {"response": data.get("text", "")}
    
    # Add the new message to the list
    messages.append(new_message)
    
    # Check for specific keywords and set the page to load
    page_to_load = None
    if "material simulation" in new_message["response"].lower():
        page_to_load = "materialsim"
    elif "material discovery" in new_message["response"].lower():
        page_to_load = "materialdis"
    elif "sustainability testing" in new_message["response"].lower():
        page_to_load = "sustaintest"
    elif "material performance" in new_message["response"].lower():
        page_to_load = "materialperf"
    elif "lab equipment" in new_message["response"].lower():
        page_to_load = "iot"  # Direct to IoT page for device-related messages
    
    # Include the page_to_load flag in the response
    new_message["page_to_load"] = page_to_load
    
    # Notify subscribers (optional, not required for AJAX)
    for subscriber in subscribers:
        subscriber.put(new_message["response"])
    
    return jsonify(new_message), 200

@app.route('/sustaintest')
def sustaintest():
    return render_template('sustaintest.html')

@app.route('/materialperf')
def materialperf():
    return render_template('materialperf.html')

@app.route('/history')
def history():
    # Return the full message history as JSON
    return jsonify(messages)

# Add route for serving materialdis.html
@app.route('/materialdis')
def materialdis():
    return render_template('materialdis.html')

@app.route('/events')
def events():
    def generate():
        while True:
            if messages:
                new_message = messages[-1]  # Get latest message
                yield f"data: {new_message['response']}\n\n"
            time.sleep(2)  # Update every 2 seconds or based on your own condition
        return Response(generate(), content_type='text/event-stream')

@app.route('/materialsim')
def materialsim():
    return render_template('materialsim.html')

# Simulated database for devices
devices = {
    "oven01": {"status": "off", "performance": {"temperature": 25.0, "usageTime": 0, "errors": []}},
    "microscope02": {"status": "off", "performance": {"temperature": None, "usageTime": 10, "errors": []}},
    "centrifuge03": {"status": "off", "performance": {"temperature": 20.0, "usageTime": 5, "errors": ["Maintenance required"]}},
}

# Control a specific IoT device
@app.route('/devices/<deviceId>/control', methods=['POST'])
def control_device(deviceId):
    action = request.json.get("action")
    
    if not action or action not in ["turn_on", "turn_off"]:
        return jsonify({"error": "Invalid action. Use 'turn_on' or 'turn_off'."}), 400
    
    device = devices.get(deviceId)
    if not device:
        return jsonify({"error": f"Device with ID {deviceId} not found."}), 404

    # Update device status based on the action
    if action == "turn_on":
        device["status"] = "on"
    elif action == "turn_off":
        device["status"] = "off"
    
    # Send the device status update to all subscribers
    for subscriber in subscribers:
        subscriber.put(f"Device {deviceId} status: {device['status']}")
    
    return jsonify({
        "deviceId": deviceId,
        "action": action,
        "status": device["status"]
    }), 200

# Get the status of a specific IoT device
@app.route('/devices/<deviceId>/status', methods=['GET'])
def get_device_status(deviceId):
    device = devices.get(deviceId)
    if not device:
        return jsonify({"error": f"Device with ID {deviceId} not found."}), 404
    
    return jsonify({
        "deviceId": deviceId,
        "status": device["status"],
        "performance": device["performance"]
    }), 200

# Health check endpoint (optional)
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Home route serving an HTML template for IoT
@app.route('/iot')
def iot():
    return render_template('iot.html')

if __name__ == '__main__':
    app.run(debug=True)
