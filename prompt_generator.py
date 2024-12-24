import requests
import sqlite3

class GTOPromptGenerator:
    def __init__(self, gto_wizard_url, pt4_db_path):
        self.gto_wizard_url = gto_wizard_url
        self.pt4_db_path = pt4_db_path

    def fetch_gto_ranges(self):
        try:
            response = requests.get(self.gto_wizard_url)
            response.raise_for_status()
            gto_data = response.json()
            return gto_data
        except requests.RequestException as e:
            print(f"Error fetching GTO ranges: {e}")
            return None

    def fetch_player_stats(self):
        try:
            conn = sqlite3.connect(self.pt4_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM player_stats")  # Example query
            player_stats = cursor.fetchall()
            conn.close()
            return player_stats
        except sqlite3.Error as e:
            print(f"Error accessing PokerTracker 4 database: {e}")
            return None

    def generate_prompt(self):
        gto_ranges = self.fetch_gto_ranges()
        player_stats = self.fetch_player_stats()

        if not gto_ranges or not player_stats:
            return "Error generating prompt due to data retrieval issues."

        # Example logic to generate a prompt
        prompt = "Based on the GTO ranges and player stats, the recommended strategy is:\n"
        for stat in player_stats:
            prompt += f"Player {stat[0]}: Adjust strategy based on {gto_ranges.get('strategy', 'default strategy')}.\n"

        return prompt

if __name__ == "__main__":
    gto_wizard_url = "https://app.gtowizard.com/solutions?tmpId=1735030971434&solution_type=gwiz&soltab=strategy&gmfs_solution_tab=ai_sols&gametype=SpinsGeneralV2&depth=25&stacks=25-25-25&gmff_stacks_type=SYMMETRIC&gmff_biggest_stack=25&gmff_favorite=false&gmfft_sort_key=0&gmfft_sort_order=desc&history_spot=0"
    pt4_db_path = "path_to_pokertracker4_database.db"

    generator = GTOPromptGenerator(gto_wizard_url, pt4_db_path)
    prompt = generator.generate_prompt()
    print(prompt)
