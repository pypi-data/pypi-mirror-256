if [ "${1}" == "prod" ]; then
	# ATTENTION: For production environment
	export AZURE_CLIENT_ID=240a6670-3b8b-45c1-ba8c-24fccc006987
	export AZURE_TENANT_ID=eb06985d-06ca-4a17-81da-629ab99f6505
	export AZURE_CLIENT_SECRET=H.0f65NR-zLq6QM5a5Zz_x~6MI9eaHZdqw
else
	export AZURE_CLIENT_ID=f30ea6ca-bd5f-4c22-ab43-217a1275cde9
	export AZURE_TENANT_ID=eb06985d-06ca-4a17-81da-629ab99f6505
	export AZURE_CLIENT_SECRET=H3JZi.-P6mr3CYl4G5.Js84ZLLEh_PuQ9e
fi
