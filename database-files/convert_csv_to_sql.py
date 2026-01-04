import csv
import os

# Folder containing your CSV files
FOLDER = os.path.dirname(os.path.abspath(__file__))

def convert_csv_to_sql(csv_path):
    table_name = os.path.splitext(os.path.basename(csv_path))[0]  # filename becomes table name
    sql_path = csv_path.replace(".csv", ".sql")

    with open(csv_path, "r", newline='', encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        columns = reader.fieldnames

        with open(sql_path, "w", encoding="utf-8") as outfile:
            for row in reader:
                values = []
                for col in columns:
                    val = row[col]
                    if val == "" or val.lower() == "null":
                        values.append("NULL")
                    else:
                        # escape single quotes
                        val = val.replace("'", "''")
                        values.append(f"'{val}'")

                col_string = ", ".join(columns)
                val_string = ", ".join(values)

                outfile.write(
                    f"INSERT INTO {table_name} ({col_string}) VALUES ({val_string});\n"
                )

    print(f"Created: {sql_path}")


def main():
    for filename in os.listdir(FOLDER):
        if filename.lower().endswith(".csv"):
            convert_csv_to_sql(os.path.join(FOLDER, filename))


if __name__ == "__main__":
    main()
