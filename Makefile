ME = $(shell pwd | sed -e 's/\//\\\//g')

install:
	@echo "Installing .desktop file in "$(HOME)"/.local/share/applications/facebook.desktop"
	@cat facebook.desktop | sed -e "s/Exec=/Exec=$(ME)\//g" -e 's/Icon=facebook/Icon=$(ME)\/icons\/hicolor\/48x48\/apps\/facebook.png/g' > $(HOME)/.local/share/applications/facebook.desktop

	# open web browser added by hany
	@xdg-open "https://www.facebook.com/dialog/oauth?client_id=cf61e1494a431f7db3c8372cc4a17bdf&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token&scope=read_mailbox,read_requests,offline_access,manage_notifications,user_photos,user_activities,user_likes,user_photos"

uninstall:
	@echo "Removing .desktop file from "$(HOME)"/.local/share/applications/facebook.desktop"
	@rm -f $(HOME)/.local/share/applications/facebook.desktop