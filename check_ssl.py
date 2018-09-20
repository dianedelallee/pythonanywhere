import subprocess
from datetime import datetime, timedelta

import os

if __name__ == '__main__':

    web_apps = ["www.app1.ch", "www.app_2.ch"]
    os.chdir('letsencrypt')

    for app in web_apps:
        bash_command = "echo $(openssl x509 -enddate -noout -in ~/letsencrypt/{}/cert.pem)".format(app)
        process = subprocess.check_output(['bash','-c', bash_command])
        process = process.decode("utf-8")
        process = process.replace('\n', '')
        res = process.split("notAfter=")

        datetime_object = datetime.strptime(res[1], '%b %d %H:%M:%S %Y %Z')
        td = timedelta(days=2)
        delta = datetime_object - td

        if datetime.now() >= delta:    # renew the certificate
            print('We will renew the certificate for {}'.format(app))
            try:
                bash_command_renew_certificate = '~/dehydrated/dehydrated --cron --domain {} --out . --challenge http-01'.format(app)
                bash_command_install_certificate = 'pa_install_webapp_letsencrypt_ssl.py {}'.format(app)
                subprocess.check_output(['bash','-c', bash_command_renew_certificate])
                subprocess.check_output(['bash','-c', bash_command_install_certificate])
                print('Certificate renewed for {}'.format(app))
            except Exception as e:
                print(e)
                print('Certificate not renewed for {}'.format(app))

        else:
            print("The certificate for {} is up to date !".format(app))
            print("It will expired the {}".format(datetime_object))
        print(20*'----')
