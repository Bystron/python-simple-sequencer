import rtmidi
import time
import threading


# Function to play a sequence of notes
def play_notes(output, sequence):
    while True:
        for note, duration in sequence:
            # Note on
            output.send_message([0x90, note, 112])  # Channel 1, velocity 112
            time.sleep(duration)
            # Note off
            output.send_message([0x80, note, 0])  # Channel 1, velocity 0


# Function to get user input and update the sequence
def get_user_input(sequence):
    while True:
        try:
            note = int(input("Enter MIDI note number (0-127): "))
            duration = float(input("Enter note duration (seconds): "))
            sequence.append((note, duration))
            print(f"Added note {note} with duration {duration}s")
        except ValueError:
            print("Invalid input. Please enter a valid note number and duration.")


# Main function
def main():
    # Create a MIDI output object
    midiout = rtmidi.MidiOut()

    # List available output ports
    available_ports = midiout.get_ports()
    if available_ports:
        print("Available MIDI output ports:")
        for i, port in enumerate(available_ports):
            print(f"{i}: {port}")

        # Prompt user to select a port
        port_index = int(input("Select a MIDI output port by index: "))
        if port_index < 0 or port_index >= len(available_ports):
            print("Invalid port index.")
            return
    else:
        print("No available MIDI output ports.")
        return
    # Open the selected port
    try:
        midiout.open_port(port_index)
    except Exception as e:
        print(f"Error opening MIDI port: {e}")
        return

    # Initialize an empty sequence
    sequence = []

    # Start the playback thread
    playback_thread = threading.Thread(target=play_notes, args=(midiout, sequence))
    playback_thread.daemon = True  # This thread will exit when the main thread does
    playback_thread.start()

    # Start the user input loop
    get_user_input(sequence)

    # Close the port (although this will never be reached in this simple loop)
    midiout.close_port()


if __name__ == "__main__":
    main()
