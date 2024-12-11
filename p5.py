# Develop a simple data link layer that performs the flow control using the sliding window protocol, and loss recovery using the Go-Back-N mechanism.

def send_frames(frames, window_size):
    i = 0
    n = len(frames)

    print("\nWith sliding window protocol the frames will be sent in the following manner (assuming no corruption of frames)\n")
    print(f"After sending {
          window_size} frames at each stage, the sender waits for acknowledgment sent by the receiver\n")

    while i < n:
        # Send frames within the window
        for j in range(i, min(i + window_size, n)):
            print(frames[j], end=' ')
        print()

        # Simulate the reception of acknowledgments
        if (i + window_size) < n:
            print("Acknowledgment of above frames sent is received by sender\n")

        i += window_size

    if n % window_size != 0:
        print("Acknowledgment of above frames sent is received by sender\n")


def main():
    window_size = int(input("Enter window size: "))
    num_frames = int(input("\nEnter number of frames to transmit: "))

    frames = []
    print(f"\nEnter {num_frames} frames: ")
    for i in range(num_frames):
        frame = int(input())
        frames.append(frame)

    send_frames(frames, window_size)


if __name__ == "__main__":
    main()
