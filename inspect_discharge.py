
import scipy.io

mat_data = scipy.io.loadmat("data/B0005.mat")
cycles = mat_data["B0005"][0, 0]["cycle"][0]

# Find the first discharge operation
for i, operation in enumerate(cycles):

    operation_type = operation["type"][0]

    if operation_type == "discharge":

        discharge_data = operation["data"][0, 0]

        print("First discharge operation:", i + 1)
        print("\nAvailable measurement fields:")
        print(discharge_data.dtype.names)

        print("\nMeasurement information:")

        for field in discharge_data.dtype.names:
            value = discharge_data[field]

            print(
                field,
                "Shape:",
                value.shape,
                "Data type:",
                value.dtype
            )

        break
