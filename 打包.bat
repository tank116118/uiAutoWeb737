cd I:\pythonProject\tank\telegramAuto
pyinstaller -D --collect-all poetry `
--hidden-import=Business.controller.telegram.accountCtrl `
--hidden-import=Business.controller.telegram.groupCtrl `
--hidden-import=Business.controller.telegram.robotCtrl `
--hidden-import=Business.controller.whatsapp.accountCtrl `
--hidden-import=Business.controller.whatsapp.groupCtrl `
--hidden-import=Business.controller.google.accountCtrl `
--add-data=./Static:./Static --add-data=C:/Users/Admin/AppData/Local/ms-playwright:./playwright/driver/package/.local-browsers uiAuto.py