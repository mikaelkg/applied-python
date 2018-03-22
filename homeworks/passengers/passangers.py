# -*- encoding: utf-8 -*-


def process(data, events, car):
    
    def find_passenger(passenger,data):
        for num_train,train in enumerate(data):
            for num_car,car in enumerate(train['cars']):
                if passenger in car['people']:
                    return [num_train,num_car]
        else:
            return [None,None]

    def find_train(train_name,data):
        for num_train,train in enumerate(data):
            if train['name']==train_name:
                return num_train

    def detach_cars(count,data,train_from):
        detached_cars=[]
        for i in range(count):
            detached_cars.append(data[train_from]['cars'].pop())
        return detached_cars[::-1]

    def attach_cars(cars,data,train_to):
        for car in cars:
            data[train_to]['cars'].append(car)
            
    def count_in_car(car_name,data):
        for train in data:
            for car in train['cars']:
                if car['name']==car_name:
                    return len(car['people'])
    for event in events:
        if event['type']=='walk':
            passenger=event["passenger"]
            train_num,car_num=find_passenger(passenger,data)
            if train_num==None:
                return -1
            data[train_num]['cars'][car_num]['people'].remove(passenger)
            move=event["distance"]+car_num
            if move<0 or move>=len(data[train_num]['cars']):
                return -1
            data[train_num]['cars'][move]['people'].append(passenger)

        elif event['type']=='switch':
            count=event['cars']
            train_from=find_train(event['train_from'],data)
            train_to=find_train(event['train_to'],data)
            if train_from==None or train_to==None:
                return -1
            elif len(data[train_from]['cars'])<count:
                return -1
            detached_cars=detach_cars(count,data,train_from)
            attach_cars(detached_cars,data,train_to)
  
    return count_in_car(car,data)