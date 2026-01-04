import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📹 Live Game Scout')
st.write('Tag and annotate plays during live games')

scout_id = st.session_state.get('user_id', 1)

# Game selection
st.write("### Select Game to Scout")

try:
    # Get scout's game history to show available games
    response = requests.get(f'http://web-api:4000/scouts/{scout_id}/game_history')

    if response.status_code == 200:
        games = response.json()

        if games:
            game_options = {
                f"Game #{g['gameID']} - {g.get('date', 'N/A')} vs {g.get('opponent', 'Unknown')}": g['gameID']
                for g in games
            }

            selected_game_str = st.selectbox("Select Game", list(game_options.keys()))
            game_id = game_options[selected_game_str]
        else:
            st.info("No games in history. Enter a game ID manually:")
            game_id = st.number_input("Game ID", min_value=1, value=1)
    else:
        game_id = st.number_input("Game ID", min_value=1, value=1)

except Exception as e:
    st.warning(f"Could not load games: {str(e)}")
    game_id = st.number_input("Game ID", min_value=1, value=1)

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### Game Feed")

    try:
        # Get game footage for this game
        footage_response = requests.get(f'http://web-api:4000/players/1/videos')

        if footage_response.status_code == 200:
            footage_list = footage_response.json()
            game_footage = [f for f in footage_list if f.get('gameID') == game_id]

            if game_footage:
                st.success("Game footage available")
                for footage in game_footage[:3]:
                    st.video(footage['URL'])
            else:
                st.info("No footage available for this game yet")
        else:
            st.info("Live game video would appear here")
    except:
        st.info("Live game video would appear here")

    st.write(f"**Game #{game_id}**")
    st.write("Scouting in progress...")

with col2:
    st.write("### Quick Tags")

    # Quick tag buttons with automatic annotation
    tag_buttons = st.columns(3)
    with tag_buttons[0]:
        if st.button("Fast Break", use_container_width=True, key="fast_break"):
            quick_annotation = {
                'gameID': game_id,
                'playerID': None,
                'annotatedBy': scout_id,
                'text': 'Fast Break',
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            try:
                response = requests.post(
                    f'http://web-api:4000/scouts/{scout_id}/annotations',
                    json=quick_annotation
                )
                if response.status_code == 201:
                    st.success("Tagged!")
                    st.rerun()
                else:
                    st.error(f"Failed: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    with tag_buttons[1]:
        if st.button("Assist", use_container_width=True, key="assist"):
            quick_annotation = {
                'gameID': game_id,
                'playerID': None,
                'annotatedBy': scout_id,
                'text': 'Great Assist',
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            try:
                response = requests.post(
                    f'http://web-api:4000/scouts/{scout_id}/annotations',
                    json=quick_annotation
                )
                if response.status_code == 201:
                    st.success("Tagged!")
                    st.rerun()
                else:
                    st.error(f"Failed: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    with tag_buttons[2]:
        if st.button("Rebound", use_container_width=True, key="rebound"):
            quick_annotation = {
                'gameID': game_id,
                'playerID': None,
                'annotatedBy': scout_id,
                'text': 'Strong Rebound',
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            try:
                response = requests.post(
                    f'http://web-api:4000/scouts/{scout_id}/annotations',
                    json=quick_annotation
                )
                if response.status_code == 201:
                    st.success("Tagged!")
                    st.rerun()
                else:
                    st.error(f"Failed: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Annotation form
st.write("---")
st.write("### Add Detailed Annotation")
st.info("💡 Add notes about specific plays or moments during the game")

with st.form("annotation_form"):
    col1, col2 = st.columns(2)

    with col1:
        player_id = st.number_input("Player ID (Optional)", min_value=0, value=0,
                                    help="Leave as 0 for general game notes")
        timestamp = st.text_input("Timestamp (HH:MM:SS)", value="00:00:00",
                                  help="Time in the game when this play occurred")

    with col2:
        play_type = st.selectbox("Play Type",
                                 ["General", "Offensive", "Defensive", "Transition", "Set Play"])

    note = st.text_area("Detailed Notes",
                        placeholder="e.g., 'Great defensive rotation - closed out on shooter with quick feet'",
                        height=100)

    if st.form_submit_button("Save Annotation", type="primary"):
        if not note:
            st.error("⚠️ Please enter annotation notes")
        else:
            try:
                annotation_data = {
                    'gameID': game_id,
                    'playerID': int(player_id) if player_id > 0 else None,
                    'annotatedBy': scout_id,
                    'text': f"[{play_type}] {note}",
                    'timestamp': timestamp
                }

                response = requests.post(
                    f'http://web-api:4000/scouts/{scout_id}/annotations',
                    json=annotation_data
                )

                if response.status_code == 201:
                    st.success("✅ Annotation saved!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Failed to save annotation: {response.status_code}")
                    st.error(f"Error: {response.text}")

            except Exception as e:
                st.error(f"Error saving annotation: {str(e)}")

# Recent annotations for this game
st.write("---")
st.write(f"### Annotations for Game #{game_id}")

try:
    # Fetch annotations for current game
    annotations_response = requests.get(f'http://web-api:4000/games/{game_id}/annotations')

    if annotations_response.status_code == 200:
        annotations_data = annotations_response.json()

        if annotations_data:
            df = pd.DataFrame(annotations_data)
            # Select relevant columns
            display_cols = ['timestamp', 'text', 'scout_first', 'scout_last', 'player_first', 'player_last']
            available_cols = [col for col in display_cols if col in df.columns]
            if available_cols:
                st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No annotations yet for this game. Add your first one above!")
    else:
        st.info("Annotations will appear here once you add them")

except Exception as e:
    st.info("Annotations will appear here once you add them")

# Scout activity logging
st.write("---")
st.write("### Scout Activity")

try:
    response = requests.get(f'http://web-api:4000/scouts/{scout_id}/game_history')

    if response.status_code == 200:
        games_attended = response.json()

        if games_attended:
            st.success(f"You have scouted {len(games_attended)} games")

            recent_df = pd.DataFrame(games_attended)
            if 'date' in recent_df.columns:
                display_cols = ['gameID', 'date', 'opponent', 'venue']
                available_cols = [col for col in display_cols if col in recent_df.columns]
                display_df = recent_df[available_cols].copy()
                st.dataframe(display_df.head(5), use_container_width=True, hide_index=True)
        else:
            st.info("No games scouted yet")
    else:
        st.info("Scout activity data unavailable")

except Exception as e:
    st.info("Scout activity data unavailable")

# Tips
st.write("---")
st.write("### 📌 Scouting Tips")
st.info("""
- Use Quick Tags for rapid notation during live games
- Add detailed notes with timestamps for important moments
- Document both strengths and areas for improvement
- Note defensive rotations, offensive sets, and transition plays
- Review annotations after the game for comprehensive reports
""")
