from services.get_user_top_following_accounts import get_user_top_following_accounts
from services.get_user_medias import get_user_medias

""" local variables """
user_ids = ["17368259", "1681595742018756608"]


def main():
    for user_id in user_ids:
        all_user_medias = get_user_medias(user_id)
        print(all_user_medias)

        all_following_accounts = get_user_top_following_accounts(user_id)
        print(all_following_accounts)


if __name__ == "__main__":
    main()
