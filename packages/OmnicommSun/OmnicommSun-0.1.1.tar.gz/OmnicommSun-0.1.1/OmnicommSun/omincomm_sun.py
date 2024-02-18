from datetime import datetime
import json
import requests as r


class SUN:
    URL = "https://config.omnicomm.ru/api"
    params_description = {
        'grid': {
            'firmwareVersion': 'Версия прошивки',
            'lastRecord': 'Номер последней записи',
            'settingsVersion': 'Версия настроек',
            'lastChange': 'Последняя смена настроек',
            'lastAuth': 'Последний выход на связь',
            'lastInteractionWithCS': 'Последний выход на связь с КС',
            'csLastDataTimestamp': 'Дата последней переданной записи на КС',
            'unlockDate': 'Блокировка',
            'ID': 'ID регистратора',
        },
        'params': {
            'gprs_settings': {
                'access_point_string': 'Имя точки доступа',
                'phone_number': 'Телефонный номер',
                'iccid': 'ICCID',
                'gprs_login': 'Логин',
                'gprs_password': 'Пароль'
            },
            'cs_settings': {
                'ip_domain': 'IP адрес или доменное имя',
                'port': 'Порт',
                'protocol': 'Протокол'
            },
            'egts_settings-tid': 'Настройки протокола EGTS',
            'data_accumulation': {
                'outliers_filtering': 'Фильтрация выбросов координат',
                'accumulate_if': 'Собирать данные при выкл. зажигании',
                'adaptive_accumulation': 'Адаптивный сбор данных на поворотах',
                'timer': 'Таймер сбора данных',
                'sleepperiod': 'Период отправки данных на сервер',
                'probeg': 'Пробег между точками, м',
                'accumulate_all': 'Собирать все данные',
                'distance_accumulation': 'Сбор данных по пройденному расстоянию',
                'ignition_timeout': 'Задержка после вкл. зажигания',
                'max_speed': 'Максимальная скорость перемещения'
            },
            'networking-period': 'Период отправки данных на КС (мин)',
            'roaming_switch': {
                'sim1_list': 'Список сим для роуминга 1',
                'sim2_list': 'Список сим для роуминга 2',
                'sim1': 'Роуминг для сим 1',
                'sim2': 'Роуминг для сим 2'
            },
            'rouming_networking': {
                'connection_onevent': 'Выход на связь по событию',
                'period': 'Период отправки данных на КС (мин)',
                'size': 'Размер пакета данных для передачи на КС (килобайт)'
            },
            'networking_gsm_sms': {
                'garniture': 'Гарнитура',
                'dispatcher_number': 'Номер диспетчера',
                'sms': 'СМС',
                'vehicle_name': 'Название ТС',
                'sms_lang': 'Язык шаблона СМС',
                'sms_number': 'Номер для отправки СМС'
            },
            'enter_loops_settings': {
                'signal': 'Тип сигнала',
                'coef': 'Коэффициент калибровки оборотов',
                'toto': 'Подтяжка'
            },
            'enter_speed_settings': {
                'type': 'Режим работы',
                'coef': 'Коэффициент калибровки',
                'sound': 'Звуковое уведомление при превышении',
                'maxspeed': 'Максимальная разрешенная скорость, км/ч',
                'speedlimit': 'Порог включения уведомления'
            },
            'uv': {
                'uv': 'Состояние',
                'inversion': 'Инверсия',
                'minU': 'Напряжение, соответствующее минимальному значению',
                'maxU': 'Напряжение, соответствующее максимальному значению',
                'coef': 'Коэффициент калибровки',
                'toto': 'Подтяжка',
                'speedthreshold': 'Порог скорости',
                'min': 'Минимальное значение величины',
                'max': 'Максимальное значение величины',
                'speedthresholdswitch': 'Использовать порог скорости',
                'precision': 'Точность',
                'name': 'Имя оборудования',
                'sms': 'Отправка SMS',
                'limiton': 'Порог напряжения включения',
                'type': 'Режим работы'
            },
            'fuel_params': {
                'count': 'Количество датчиков',
                'filter': 'Фильтрация',
                'type': 'Тип датчиков',
                'tank_volume': 'Объем бака'
            },
            'ignition': {
                'level': 'Порог включения зажигания',
                'source': 'Источник данных'
            },
            'rs': {
                'rs485': 'RS485 №1',
                'rs485_2': 'RS485 №2',
                'rs232_1': 'RS232 №1',
                'rs232_2': 'RS232 №2',
                'rs_speed_nmea': 'Скорость'
            },
            'wifi': {
                'password': 'Пароль',
                'switcher': 'Модуль Wi-Fi',
                'ssid': 'SSID',
                'login': 'Логин',
                'key': 'Ключ',
                'security_method': 'Метод шифрования'
            }
        }
    }

    def __init__(self):
        self._start()

    def _start(self):
        params = f'{self.URL}?action=locale&lang=ru'
        r.post(params)

    def _get_task_queue(self):
        data = {
            "action": "getTaskQueue"
        }
        response = r.post(url=self.URL, data=data)
        return response

    def get_registrator_settings(self, terminal_id: int, password: str):
        """
        :param terminal_id: номер терминала
        :param password: пароль
        :return: настройки терминала
        """
        data = {
            "action": "getRegistrator",
            "data": json.dumps({
                "ID": terminal_id,
                "password": password,
                "registratorid": []
            })
        }
        response = r.post(url=self.URL, params=data)
        return response.json()['response']

    def get_params_list(self):
        params = ['grid']
        params += [p for p in self.params_description['params'].keys()]
        return params

    def get_description_params(self, data, key):
        descript = {}
        if key == 'all':
            for p in self.get_params_list():
                descript.update(self.get_description_params(data, p))
            return descript
        elif key == 'grid':
            datetime_params = [
                'lastAuth',
                'lastInteractionWithCS',
                'lastChange',
                'csLastDataTimestamp',
            ]
            for param in data[key].keys():
                try:
                    param_name = self.params_description['grid'][param]
                    value = data['grid'][param]
                    if param in datetime_params:
                        if value <= 0:
                            value = ''
                        else:
                            value = datetime.utcfromtimestamp(int(value)/1000 + 10800).strftime('%d.%m.%Y %H:%M:%S')
                    descript[param] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'gprs_settings':
            for i in range(1, 4):
                for param in self.params_description['params'][key].keys():
                    try:
                        param_name = self.params_description['params'][key][param] + ' ' + str(i)
                        if param == 'iccid':
                            param = 'iccid' + str(i-1)
                        param_code = key + '-' + param
                        if i != 1:
                            param_code = 'gprs_' + str(i) + '_settings-' + param
                        value = data['params'][param_code]
                        descript[param_code] = {
                            'descript_name': param_name,
                            'value': value
                        }
                    except KeyError:
                        continue
        elif key == 'cs_settings':
            param_protocol = {
                '0': 'Omnicomm',
                '1': 'EGTS'
            }
            for i in range(1, 4):
                for param in self.params_description['params'][key].keys():
                    try:
                        param_name = self.params_description['params'][key][param] + ' ' + str(i)
                        param_code = key + '-' + param
                        if i != 1:
                            param_code = 'cs' + str(i) + '_settings-' + param
                        value = data['params'][param_code]
                        if param == 'protocol':
                            value = param_protocol[value]
                        descript[param_code] = {
                            'descript_name': param_name,
                            'value': value
                        }
                    except KeyError:
                        continue
        elif key == 'data_accumulation':
            for param in self.params_description['params'][key].keys():
                param_accumulation = {
                    '0': 'Собирать все данные',
                    '1': 'Собирать данные при тряске',
                    '2': 'Собирать все кроме GPS'
                }
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if param == 'accumulate_if':
                        value = param_accumulation[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'roaming_switch':
            param_roaming = {
                '0': 'Запрещен',
                '1': 'Разрешен',
                '2': 'Разрешен по списку'
            }
            for param in self.params_description['params'][key].keys():
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if 'sim' in param and 'list' not in param:
                        value = param_roaming[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'rouming_networking':
            param_connection = {
                '0': 'Период отправки',
                '1': 'Размер пакета',
            }
            for param in self.params_description['params'][key].keys():
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if param == 'connection_onevent':
                        value = param_connection[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'networking_gsm_sms':
            param_lang = {
                '0': 'Русский',
                '1': 'Английский',
                '2': 'Португальский',
                '3': 'Испанский'
            }
            for param in self.params_description['params'][key].keys():
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if param == 'sms_lang':
                        value = param_lang[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'enter_loops_settings':
            param_signal = {
                '0': 'Выключен',
                '1': 'Вход оборотов',
                '2': 'Ключ зажигания',
                '3': 'Шина CAN'
            }
            for param in self.params_description['params'][key].keys():
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if param == 'signal':
                        value = param_signal[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'enter_speed_settings':
            param_type = {
                '0': 'GPS',
                '1': 'УВ-6',
                '2': 'Шина CAN'
            }
            for param in self.params_description['params'][key].keys():
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if param == 'type':
                        value = param_type[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'uv':
            param_precision = {
                '0': '0 (1)',
                '1': '1 (0.1)',
                '2': '2 (0.01)',
                '3': '3 (0.001)',
            }
            param_type = {
                '0': 'Аналоговый',
                '1': 'Потенциальный',
                '2': 'Импульсный',
                '3': 'Частотный',
                '4': '1-wire',
            }
            for i in range(1, 13):
                for param in self.params_description['params'][key].keys():
                    try:
                        param_name = self.params_description['params'][key][param] + ' УВ ' + str(i)
                        param_code = key + str(i) + '-' + param
                        value = data['params'][param_code]
                        if param == 'precision':
                            value = param_precision[value]
                        if param == 'type':
                            value = param_type[value]
                        descript[param_code] = {
                            'descript_name': param_name,
                            'value': value
                        }
                    except KeyError:
                        continue
        elif key == 'fuel_params':
            param_type = {
                '0': 'Цифровой LLS',
                '1': 'Частотный LLS-AF',
                '2': 'Аналоговый (штатный)',
                '3': 'Шина CAN',
                '4': 'Выключен',
                '5': 'Струна+',
                '6': 'ПМП-201',
            }
            for param in self.params_description['params'][key].keys():
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if param == 'type':
                        value = param_type[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'ignition':
            param_source = {
                '0': 'Напряжение бортовой сети',
                '1': 'Ключ зажигания',
            }
            for param in self.params_description['params'][key].keys():
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if param == 'source':
                        value = param_source[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'rs':
            param_rs = {
                '0': 'Выключен',
                '1': 'CAN-LOG',
                '2': 'J1708',
                '3': 'NMEA прием',
                '4': 'NMEA передача',
                '5': 'ПП-01',
                '6': 'Фотокамера',
                '7': 'DV-1',
                '8': 'LLS/LLD',
                '9': 'TPMS "Pressure Pro"',
                '10': 'Modbus (Струна+, ПМП-201)',
            }
            for param in self.params_description['params'][key].keys():
                try:
                    param_name = self.params_description['params'][key][param]
                    param_code = key + '-' + param
                    value = data['params'][param_code]
                    if 'rs_speed_nmea' not in param:
                        value = param_rs[value]
                    descript[param_code] = {
                        'descript_name': param_name,
                        'value': value
                    }
                except KeyError:
                    continue
        elif key == 'wifi':
            param_security_method = {
                '0': 'Open',
                '1': 'WPA-PSK',
                '2': 'WPA-EAP(FAST)',
                '3': 'WPA-EAP(PEAP)',
            }
            for i in range(1, 10):
                for param in self.params_description['params'][key].keys():
                    try:
                        param_name = self.params_description['params'][key][param] + ' ' + str(i)
                        param_code = key + '-' + param + str(i)
                        if param == 'switcher':
                            param_name = self.params_description['params'][key][param]
                            param_code = key + '-' + param
                        value = data['params'][param_code]
                        if param == 'security_method':
                            value = param_security_method[value]
                        descript[param_code] = {
                            'descript_name': param_name,
                            'value': value
                        }
                    except KeyError:
                        continue
        else:
            try:
                param_name = self.params_description['params'][key]
                descript[key] = {
                    'descript_name': param_name,
                    'value': data['params'][key]
                }
            except KeyError:
                pass
        
        return descript










