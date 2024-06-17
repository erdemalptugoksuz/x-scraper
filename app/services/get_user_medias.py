"""
    This module attempts to retrieve the profile medias.
"""

import requests
import os
import json

from dotenv import load_dotenv
load_dotenv()

""" environment variables """
X_AUTHORIZATION_TOKEN = os.getenv('X_AUTHORIZATION_TOKEN')
X_COOKIE_TOKEN = os.getenv('X_COOKIE_TOKEN')
X_CSRF_TOKEN = os.getenv('X_CSRF_TOKEN')


def get_user_medias(user_id):
    all_medias = []

    variables = json.dumps({"userId": user_id, "count": 100, "includePromotedContent": False,
                           "withClientEventToken": False, "withBirdwatchNotes": False, "withVoice": True, "withV2Timeline": True})
    features = json.dumps({"rweb_tipjar_consumption_enabled": True, "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False, "creator_subscriptions_tweet_preview_api_enabled": True, "responsive_web_graphql_timeline_navigation_enabled": True, "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False, "communities_web_enable_tweet_community_results_fetch": True, "c9s_tweet_anatomy_moderator_badge_enabled": True, "articles_preview_enabled": True, "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True, "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                          "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True, "responsive_web_twitter_article_tweet_consumption_enabled": True, "tweet_awards_web_tipping_enabled": False, "creator_subscriptions_quote_tweet_preview_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True, "standardized_nudges_misinfo": True, "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True, "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True, "longform_notetweets_inline_media_enabled": True, "responsive_web_enhance_cards_enabled": False})
    fieldToggles = json.dumps({"withArticlePlainText": False})

    url = "https://x.com/i/api/graphql/MOLbHrtk8Ovu7DUNOLcXiA/UserMedia"
    params = {"variables": variables,
              "features": features, "fieldToggles": fieldToggles}
    headers = {"authorization": X_AUTHORIZATION_TOKEN,
               "cookie": X_COOKIE_TOKEN, "x-csrf-token": X_CSRF_TOKEN}
    bottom_cursor = None

    try:
        while True:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if bottom_cursor is None:
                    medias = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][-1]["entries"][0]["content"]["items"]
                    bottom_cursor = data["data"]["user"]["result"]["timeline_v2"][
                        "timeline"]["instructions"][-1]["entries"][-1]["content"]["value"]
                else:
                    medias = data["data"]["user"]["result"]["timeline_v2"]["timeline"][
                        "instructions"][0]["moduleItems"]
                    bottom_cursor = data["data"]["user"]["result"]["timeline_v2"][
                        "timeline"]["instructions"][-1]["entries"][-1]["content"]["value"]

                params["variables"] = json.dumps({"userId": user_id, "count": 100, "includePromotedContent": False,
                                                  "withClientEventToken": False, "withBirdwatchNotes": False, "withVoice": True, "withV2Timeline": True, "cursor": bottom_cursor})

                for media in medias:
                    media = media.get("item", None).get("itemContent", None).get(
                        "tweet_results", None).get("result", None).get("legacy", None).get("entities", None).get("media", None)
                    if media is not None:
                        media = media[0]
                    else:
                        continue

                    media_type = media.get("type", None)
                    media_url = None

                    if media_type is not None and media_type == "video":
                        media_url = media.get("video_info", None).get(
                            "variants", None)[-1].get("url", None)
                    elif media_type is not None and media_type == "photo":
                        media_url = media.get("media_url_https", None)

                    all_medias.append({
                        "media_type": media_type,
                        "media_url": media_url
                    })

            else:
                print(f"Error: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    return all_medias
