"""
    This module attempts to retrieve the profile information of the relevant user, 
    as well as the accounts they follow and the information of the accounts that follow them.
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


def get_user_top_following_accounts(user_id):
    all_following_accounts = []

    variables = json.dumps({
        "userId": user_id,
        "count": 100,
        "includePromotedContent": False
    })
    features = json.dumps({
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "articles_preview_enabled": True,
        "tweetypie_unmention_optimization_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_enhance_cards_enabled": False
    })

    url = "https://x.com/i/api/graphql/7FEKOPNAvxWASt6v9gfCXw/Following"
    params = {
        "variables": variables,
        "features": features
    }
    headers = {
        "authorization": X_AUTHORIZATION_TOKEN,
        "cookie": X_COOKIE_TOKEN,
        "x-csrf-token": X_CSRF_TOKEN
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            following_accounts = data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"][-1]["entries"][:-2]

            for account in following_accounts:
                all_following_accounts.append({
                    "account_id": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("rest_id", None),
                    "account_name": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("legacy", None).get("name", None),
                    "account_username": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("legacy", None).get("screen_name", None),
                    "account_is_blue_verified": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("is_blue_verified", None),
                    "account_followers_count": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("legacy", None).get("followers_count", None),
                    "account_location": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("legacy", None).get("location", None)
                })
        else:
            print(f"Error: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    return all_following_accounts
