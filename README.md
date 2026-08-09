ejecutar appium
appium

lista de emulador 
emulator -list-avds

lista de dirvers
appium driver list

activar entorno 
source venv/Scripts/activate

iniciar emulador
emulator -avd Pixel_7

instalar apk
adb install "D:\mobile-automation\android.apk"

conoce capabilities
adb shell dumpsys window | findstr mCurrentFocus