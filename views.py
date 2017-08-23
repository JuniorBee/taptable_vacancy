class FirstStep(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        lang = 'en'
        if 'HTTP_CONTENT_LANGUAGE' in request.META:
            translation.activate(request.META['HTTP_CONTENT_LANGUAGE'])
            lang = request.META['HTTP_CONTENT_LANGUAGE']

        serializer = FirstStepSerializer(data=request.data)
        current_time = datetime.datetime.now().time()

        times = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00',
                 '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
                 '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00',
                 '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30',
                 '22:00', '22:30', '23:00', '23:30']

        error_text = {
            'az': "Seçdiyiniz gün işləmirik",
            'en': "We don't work on selected day",
            'ru': "Мы не работаем в выбранный день"
        }

        if serializer.is_valid():
            data = []

            try:
                place = Place.objects.all().filter(id=serializer.data['place_id'])[0]
            except IndexError:
                return JsonResponse({'error': 'Place does not exists'}, status=404, safe=False)

            if serializer.data['weekday'] == 1:

                if place.monday_start is not None and place.monday_end is not None:
                    start = datetime.datetime(2015, 1, 1, place.monday_start.hour, place.monday_start.minute)
                    end = datetime.datetime(2015, 1, 1, place.monday_end.hour, place.monday_end.minute)
                else:
                    return JsonResponse({'error': error_text[lang]}, status=400, safe=False)

            elif serializer.data['weekday'] == 2:

                if place.tuesday_start is not None and place.tuesday_end is not None:
                    start = datetime.datetime(2015, 1, 1, place.tuesday_start.hour, place.tuesday_start.minute)
                    end = datetime.datetime(2015, 1, 1, place.tuesday_end.hour, place.tuesday_end.minute)
                else:
                    return JsonResponse({'error': error_text[lang]}, status=400, safe=False)

            elif serializer.data['weekday'] == 3:
                if place.wednesday_start is not None and place.wednesday_end is not None:
                    start = datetime.datetime(2015, 1, 1, place.wednesday_start.hour, place.wednesday_start.minute)
                    end = datetime.datetime(2015, 1, 1, place.wednesday_end.hour, place.wednesday_end.minute)
                else:
                    return JsonResponse({'error': error_text[lang]}, status=400, safe=False)

            elif serializer.data['weekday'] == 4:
                if place.thursday_start is not None and place.thursday_start is not None:
                    start = datetime.datetime(2015, 1, 1, place.thursday_start.hour, place.thursday_start.minute)
                    end = datetime.datetime(2015, 1, 1, place.thursday_end.hour, place.thursday_end.minute)
                else:
                    return JsonResponse({'error': error_text[lang]}, status=400, safe=False)

            elif serializer.data['weekday'] == 5:
                if place.friday_start is not None and place.friday_end is not None:
                    start = datetime.datetime(2015, 1, 1, place.friday_start.hour, place.friday_start.minute)
                    end = datetime.datetime(2015, 1, 1, place.friday_end.hour, place.friday_end.minute)
                else:
                    return JsonResponse({'error': error_text[lang]}, status=400, safe=False)

            elif serializer.data['weekday'] == 6:
                if place.saturday_start is not None and place.saturday_end is not None:
                    start = datetime.datetime(2015, 1, 1, place.saturday_start.hour, place.saturday_start.minute)
                    end = datetime.datetime(2015, 1, 1, place.saturday_end.hour, place.saturday_end.minute)
                else:
                    return JsonResponse({'error': error_text[lang]}, status=400, safe=False)
            else:
                if place.sunday_start is not None and place.sunday_end is not None:
                    start = datetime.datetime(2015, 1, 1, place.sunday_start.hour, place.sunday_start.minute)
                    end = datetime.datetime(2015, 1, 1, place.sunday_end.hour, place.sunday_end.minute)
                else:
                    return JsonResponse({'error': error_text[lang]}, status=400, safe=False)

            start_index = times.index(start.strftime('%H:%M'))
            end_index = times.index(end.strftime('%H:%M'))
            last_index = 47

            request_date = datetime.datetime.strptime(serializer.data['date'], '%Y-%m-%d').date()

            if datetime.date.today() == request_date:
                if start.strftime('%H:%M') > end.strftime('%H:%M'):
                    for inx, val in enumerate(times):
                        if inx >= start_index and inx <= last_index:
                            if val > current_time.strftime('%H:%M'):
                                data.append(val)
                    for inx, val in enumerate(times):
                        if inx >= 0 and inx <= end_index:
                            data.append(val)
                else:
                    for inx, val in enumerate(times):
                        if inx >= start_index and inx <= end_index:
                            if val > current_time.strftime('%H:%M'):
                                data.append(val)
            else:
                if start.strftime('%H:%M') > end.strftime('%H:%M'):
                    for inx, val in enumerate(times):
                        if inx >= start_index and inx <= end_index:
                            data.append(val)
                    for inx, val in enumerate(times):
                        if inx >= 0 and inx <= end_index:
                            data.append(val)
                else:
                    for inx, val in enumerate(times):
                        if inx >= start_index and inx <= end_index:
                            data.append(val)

            response_data = {'error': str(""), 'data': data, 'place_is_open': False}

            current_datetime = datetime.datetime.now()
            start_datetime = datetime.datetime(current_datetime.year, current_datetime.month, current_datetime.day,
                                               start.hour, start.minute)
            end_datetime = datetime.datetime(current_datetime.year, current_datetime.month, current_datetime.day,
                                             end.hour, end.minute)

            if end.hour <= 10:
                end_datetime = end_datetime + datetime.timedelta(days=1)

            if current_datetime > start_datetime and current_datetime < end_datetime:
                response_data['place_is_open'] = True

            mp.track('data', json.dumps(response_data))

            return JsonResponse(response_data, status=200, safe=False)

        else:
            mp.track('error', json.dumps(serializer.errors))
            return JsonResponse(serializer.errors, status=400)
