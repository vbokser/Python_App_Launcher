import os


class SaveData:
    apps_to_open = []

    def __init__(self, filename="saved_data.txt"):
        self.filename = filename

    def saveData(self, apps):
        print(f"saved data to file {self.filename}")
        with open(self.filename, "w") as f:
            for app_loc, added in apps:
                f.write(app_loc + "\n")
        f.close()

    def readData(self):
        print(f"read data in from file {self.filename}")
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    app_loc = line.strip("\n")
                    if len(app_loc) > 2:  # make sure we have a longer file path than 2
                        print(f"...Reading app locations = {app_loc}")
                        self.apps_to_open.append([app_loc, "NOT_ADDED_YET"])
            f.close()

        return self.apps_to_open
