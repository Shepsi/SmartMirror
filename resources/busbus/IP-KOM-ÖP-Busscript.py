# -*- coding: utf-8 -*-

# Infos
# LocationRefs:
### Tarforst
#<Location>
#	<LocationRef>
#		<StopPlaceRef>de:07211:4208</StopPlaceRef>
#	</LocationRef>
#	<LocationName>
#		<Text>Tarforst</Text>
#		<Language>de</Language>
#	</LocationName>
#</Location>

### Mensa
#<Location>
#	<LocationRef>
#		<StopPlaceRef>de:07211:4516</StopPlaceRef>
#	</LocationRef>
#	<LocationName>
#		<Text>Mensa</Text>
#		<Language>de</Language>
#	</LocationName>
#</Location>

import requests
import datetime
from datetime import timedelta
from xml.dom import minidom

def busRequest(stopPlaceRef, LocationName, resultAmount):
	url = 'http://trias.vrn.de:8080/Middleware/Data/trias'
	headers = {'Content-Type' : 'application/xml'}
	xml = """<?xml version="1.0" encoding="utf-8" ?>
	<Trias xmlns="trias" xmlns:siri="http://www.siri.org.uk/siri" version="1.0">
		<ServiceRequest>
			<siri:RequestTimestamp>2016-12-12T13:42:55 </siri:RequestTimestamp>
			<siri:RequestorRef>PC-SCHWAIGER-VRT</siri:RequestorRef>
			<RequestPayload>
				<StopEventRequest>
					<Location>
						<LocationRef>
							<StopPlaceRef>""" + stopPlaceRef + """</StopPlaceRef>
						</LocationRef>
						<LocationName>
							<Text>""" + LocationName + """</Text>
							<Language>de</Language>
						</LocationName>
					</Location>
					<Params>
						<StopEventType>departure</StopEventType>
						<NumberOfResults>""" + resultAmount + """</NumberOfResults>
					</Params>
				</StopEventRequest>
			</RequestPayload>
		</ServiceRequest>
	</Trias>
	"""
	response = requests.post(url = url, data = xml, headers = headers).text
	return response

def SortOutDataFromRawXml(busrequest):
	formatedDepartureTimes = []
	rawXml = minidom.parseString(busrequest)
	arrivalsAndDeparts = rawXml.getElementsByTagName('StopEventResult')

	for stopEvent in arrivalsAndDeparts:
		# Linie
		lineNumber = stopEvent.getElementsByTagName('StopEvent')[0].getElementsByTagName('Service')[0].getElementsByTagName('PublishedLineName')[0].getElementsByTagName('Text')[0].firstChild.nodeValue
		# Ziel
		destination = stopEvent.getElementsByTagName('StopEvent')[0].getElementsByTagName('Service')[0].getElementsByTagName('DestinationText')[0].getElementsByTagName('Text')[0].firstChild.nodeValue
		#if destination == "Trier, Karl-Marx-Haus":
		#	destination = "Karl-Marx-Haus"
		#elif destination == "Kürenz, Am Weidengraben" or destination == "Kürenz, Am Weidengraben (E)":
		#	destination = " Kürenz"
		#elif destination == "Tarforst, Ludwig-Erhard-Ring":
		#	destination = " Tarforst"
		#elif destination == "Feyen, Grafschaft":
		#	destination = " Feyen"
		#elif destination == "Igel, Moselstraße":
		#	destination = " Igel"
		#elif destination == "Irsch, Hockweiler Straße":
		#	destination = " Irsch"
		
		# Abfahrtszeit + Verspätung
		estimatedArrival = stopEvent.getElementsByTagName('StopEvent')[0].getElementsByTagName('ThisCall')[0].getElementsByTagName('CallAtStop')[0].getElementsByTagName('ServiceDeparture')[0].getElementsByTagName('EstimatedTime')[0].firstChild.nodeValue
		timetabledTime = stopEvent.getElementsByTagName('StopEvent')[0].getElementsByTagName('ThisCall')[0].getElementsByTagName('CallAtStop')[0].getElementsByTagName('ServiceDeparture')[0].getElementsByTagName('TimetabledTime')[0].firstChild.nodeValue
		time = formatDatetoTime(estimatedArrival, timetabledTime)		
		formatedDepartureTimes.append(time + ' [' + lineNumber + '] ' + destination)
	return formatedDepartureTimes

def formatDatetoTime(estimatedArrival, timetabledTime):
	timetabledTime = (str(timetabledTime).split('T')[1])[:-3]
	estimatedArrival = str(estimatedArrival).split('T')[1][:-3]
	if estimatedArrival == timetabledTime:
	    return timetabledTime
	else:
		estimatedA = datetime.datetime.strptime(estimatedArrival, "%H:%M")
		timetabledT = datetime.datetime.strptime(timetabledTime, "%H:%M")
		difference = estimatedA - timetabledT
		return (estimatedArrival + "+" + str(int(difference.seconds / 60)))

def SaveDepartureTimesInTextFile(formatedDepartureTimes, locationname):
	with open("resources/busbus/" + locationname + '.txt', 'w') as outPut:
		for departureTime in formatedDepartureTimes:
			outPut.write(departureTime + '\n')

def saveBusplanAsFile(stopPlaceRef, LocationName, resultAmount):
	print("Lädt die Busse der Haltestelle " + LocationName + ".")
	busrequest = busRequest(stopPlaceRef,LocationName, resultAmount)
	print("Daten werden formatiert...")
	formatedBuslist = SortOutDataFromRawXml(busrequest)
	print("Datei wird gespeichert...")
	SaveDepartureTimesInTextFile(formatedBuslist, LocationName)

if __name__ == '__main__':
	saveBusplanAsFile("de:07211:4206", "Bonifatius", "5")
	saveBusplanAsFile("de:07211:4118","Martin-Schunck", "2")

	print('Fertig!')



### Haltestellen Id Abfragen:
#xml = """<?xml version="1.0" encoding="utf-8" ?>
#<Trias xmlns="trias" xmlns:siri="http://www.siri.org.uk/siri" version="1.0">
#    <ServiceRequest>
#        <siri:RequestTimestamp>2016-12-12T13:42:55 </siri:RequestTimestamp>
#        <siri:RequestorRef>PC-SCHWAIGER-VRT</siri:RequestorRef>
#            <RequestPayload>
#                <LocationInformationRequest>
#                    <InitialInput>
#                        <LocationName>Tarforst (Trier), Univers</LocationName>
#                    </InitialInput>
#                    <Restrictions>
#                        <Type>stop</Type>
#                        <Language>de</Language>
#                        <NumberOfResults>10</NumberOfResults>
#                    </Restrictions>
#                </LocationInformationRequest>
#        </RequestPayload>
#    </ServiceRequest>
#</Trias>
#""" 