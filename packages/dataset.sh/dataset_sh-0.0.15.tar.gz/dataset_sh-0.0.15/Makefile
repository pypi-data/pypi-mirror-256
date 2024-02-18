clean:
	rm -f dist/*
	rm src/dataset_sh/server/assets/app-ui.frontend

clean-dist:
	rm -f dist/*

frontend:
	utils/build_frontend.sh

package:
	utils/package.sh
	ll dist

upload:
	utils/upload.sh


upload-test:
	utils/upload-test.sh