import os
import pandas as pd
import glob


def collect_experiment_results(root_dir="."):
    """
    Collects all experiment results from CSV files in the specified directory structure
    and compiles them into a single DataFrame.

    Args:
        root_dir (str): Root directory containing the experiment results

    Returns:
        pd.DataFrame: DataFrame containing compiled results
    """
    # List to store all collected data
    all_data = []

    # Find all CSV files matching the pattern
    csv_pattern = os.path.join(root_dir, "*", "*", "*", "*", "*.csv")
    csv_files = glob.glob(csv_pattern)

    for csv_file in csv_files:
        # Parse directory structure to extract metadata
        parts = csv_file.split(os.sep)

        # Extract metadata from path
        architecture = parts[-5]  # courtroom or fastslow
        reflection = parts[-4] == "reflect"  # reflect or noreflect
        seed = parts[-3]  # random seed
        timestamp = parts[-2]  # timestamp

        # Load the CSV file
        try:
            df = pd.read_csv(csv_file)

            # For each row in the CSV, create a new row in our result with the metadata
            for _, row in df.iterrows():
                all_data.append(
                    {
                        "Architecture": architecture,
                        "Reflection": reflection,
                        "Random Seed": seed,
                        "Timestamp": timestamp,
                        "Won": row["custom_agent_won"],
                    }
                )
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")

    # Create a DataFrame from all collected data
    results_df = pd.DataFrame(all_data)

    return results_df


def main():
    """
    Main function to collect and export experiment results
    """
    print("Starting to collect experiment results...")

    # Collect results
    results_df = collect_experiment_results()

    # Display summary
    print(f"Collected {len(results_df)} results from experiments.")

    # Calculate win rates by architecture and reflection status
    win_rates = results_df.groupby(["Architecture", "Reflection"])["Won"].agg(
        ["count", "mean"]
    )
    win_rates.columns = ["Total Games", "Win Rate"]
    print("\nWin Rates Summary:")
    print(win_rates)

    # Export to Excel
    output_file = "ml_experiment_results.xlsx"
    results_df.to_excel(output_file, index=False)
    print(f"\nResults exported to {output_file}")


if __name__ == "__main__":
    main()
