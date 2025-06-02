import pandas as pd
import random
from collections import defaultdict

def read_data(file_path):
    # Read the data file
    df = pd.read_csv(file_path, sep='\t', header=None, 
                    names=['date', 'email', 'first_name', 'last_name', 
                          'gender', 'course', 'cohort', 'confidence'])
    
    # Clean the data
    df['name'] = df['first_name'] + ' ' + df['last_name']
    df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')
    df['course'] = df['course'].fillna('Other')
    df['cohort'] = df['cohort'].fillna('None student')
    
    return df

def categorize_individuals(df):
    # Categorize individuals by role and proficiency
    categories = {
        'Data Scientist': {'proficient': [], 'beginner': []},
        'Data Analyst': {'proficient': [], 'beginner': []},
        'Software Engineer': {'proficient': [], 'beginner': []}
    }
    
    for _, row in df.iterrows():
        # Determine role
        if row['course'] == 'Data Science':
            role = 'Data Scientist'
        elif row['course'] == 'Data Analytics':
            role = 'Data Analyst'
        else:  # 'Other' or any other value
            role = 'Software Engineer'
        
        # Determine proficiency
        proficiency = 'proficient' if row['confidence'] >= 4 else 'beginner'
        
        # Add to appropriate category
        categories[role][proficiency].append({
            'name': row['name'],
            'gender': row['gender'],
            'cohort': row['cohort'],
            'confidence': row['confidence']
        })
    
    return categories

def create_balanced_teams(categories):
    teams = []
    team_number = 1
    
    # First, create as many balanced teams as possible
    while True:
        # Check if we have enough people for a new balanced team
        if (len(categories['Data Scientist']['proficient']) < 1 or
            len(categories['Data Scientist']['beginner']) < 1 or
            len(categories['Data Analyst']['proficient']) < 1 or
            len(categories['Data Analyst']['beginner']) < 1 or
            len(categories['Software Engineer']['proficient']) < 1 or
            len(categories['Software Engineer']['beginner']) < 1):
            break
        
        # Create a new balanced team
        team = {
            'number': team_number,
            'members': []
        }
        
        # Add one proficient and one beginner from each role
        for role in categories:
            # Add proficient member
            if categories[role]['proficient']:
                member = categories[role]['proficient'].pop(0)
                team['members'].append({
                    'role': role,
                    'proficiency': 'proficient',
                    **member
                })
            
            # Add beginner member
            if categories[role]['beginner']:
                member = categories[role]['beginner'].pop(0)
                team['members'].append({
                    'role': role,
                    'proficiency': 'beginner',
                    **member
                })
        
        teams.append(team)
        team_number += 1
    
    # Create additional teams for remaining individuals
    remaining_people = []
    for role in categories:
        for proficiency in ['proficient', 'beginner']:
            remaining_people.extend([{
                'role': role,
                'proficiency': proficiency,
                **member
            } for member in categories[role][proficiency]])
    
    # Shuffle remaining people to create mixed teams
    random.shuffle(remaining_people)
    
    # Create teams of 6 from remaining people
    while remaining_people:
        team_size = min(6, len(remaining_people))
        team = {
            'number': team_number,
            'members': remaining_people[:team_size]
        }
        teams.append(team)
        remaining_people = remaining_people[team_size:]
        team_number += 1
    
    return teams

def save_teams_to_file(teams, output_file):
    with open(output_file, 'w') as f:
        for team in teams:
            f.write(f"# Team {team['number']}\n")
            for i, member in enumerate(team['members'], 1):
                f.write(f"{i}. {member['name']} ({member['role']} - {member['proficiency'].title()}, "
                       f"{member['gender']}, {member['cohort']}, Confidence: {member['confidence']})\n")
            f.write("\n")

def main():
    # Read the data
    df = read_data('t.txt')
    total_people = len(df)
    print(f"Total people in input file: {total_people}")
    
    # Categorize individuals
    categories = categorize_individuals(df)
    
    # Create teams
    teams = create_balanced_teams(categories)
    
    # Save teams to file
    save_teams_to_file(teams, 'complete_balanced_teams.txt')
    
    # Print summary
    total_teamed = sum(len(team['members']) for team in teams)
    print(f"\nCreated {len(teams)} teams")
    print(f"Total people in teams: {total_teamed}")
    print(f"All people included: {'Yes' if total_teamed == total_people else 'No'}")

if __name__ == "__main__":
    main()