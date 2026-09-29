import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------------------
# Load Flight Schedule
# ---------------------------

df = pd.read_csv("flights.csv")


def to_minutes(time_str):
    t = datetime.strptime(time_str, "%H:%M")
    return t.hour * 60 + t.minute


df["Arrival_Min"] = df["Arrival"].apply(to_minutes)
df["Departure_Min"] = df["Departure"].apply(to_minutes)

# Available gates
gates = ["A1", "A2", "A3"]

# Track the next available time for each gate
gate_availability = {gate: 0 for gate in gates}

assignments = []

# Sort flights by arrival time
df = df.sort_values("Arrival_Min")

# ---------------------------
# Assign Gates
# ---------------------------

for _, flight in df.iterrows():

    assigned_gate = None

    for gate in gates:
        # Gate is available if the previous flight
        # has already departed.
        if gate_availability[gate] <= flight["Arrival_Min"\]:
            assigned_gate = gate
            gate_availability[gate] = flight["Departure_Min"]
            break

    if assigned_gate is None:
        assigned_gate = "NO GATE AVAILABLE"

    assignments.append(assigned_gate)

df["Gate"] = assignments

# ---------------------------
# Statistics
# ---------------------------

total_flights = len(df)

assigned_flights = df[df["Gate"] != "NO GATE AVAILABLE"]

used_gates = assigned_flights["Gate"].nunique()

gate_counts = assigned_flights.groupby("Gate").size()

utilization = round(
    assigned_flights.shape[0] / (len(gates) * total_flights) * 100,
    1
)

# ---------------------------
# Display Results
# ---------------------------

print("\nFlight Gate Assignments\n")
print(df[["Flight", "Arrival", "Departure", "Gate"]])

print("\nOperational Summary")
print("-------------------")
print(f"Total Flights: {total_flights}")
print(f"Gates Used: {used_gates}")
print(f"Gate Utilization: {utilization}%")

# ---------------------------
# Visualization
# ---------------------------

plt.figure(figsize=(6, 4))

gate_counts.plot(
    kind="bar",
    color="steelblue",
    edgecolor="black"
)

plt.title("Flights Assigned per Gate")
plt.xlabel("Gate")
plt.ylabel("Number of Flights")

plt.tight_layout()

plt.savefig("gate_utilization.png")

print("\nChart saved as gate_utilization.png")
