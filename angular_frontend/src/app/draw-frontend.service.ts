import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs/internal/Observable';
import { throwError } from 'rxjs/internal/observable/throwError';
import { DoDto, ElementDto } from './types/json-response.dto';
import { Subject } from 'rxjs';
import { HttpService } from './http.service';
import { ServerRequest } from './types/server-request';
import { ContextService } from './context.service';

@Injectable({
  providedIn: 'root'
})
export class DrawFrontendService {

    frontendJson : Subject<ElementDto> = new Subject()
    menuBar: Subject<ElementDto> = new Subject()
    messageLists: Subject<ElementDto[]> = new Subject()

    private backend_URI = "http://localhost:8000"

    constructor(private httpService: HttpService, private httpClient: HttpClient, private contextService: ContextService) {
    }

    initialGet() : void {
        this.httpService.get().subscribe(
        {next: (data:ElementDto) => {
            console.log(data)
            this.frontendJson.next(data)
        }})
    }

    policyPost(callback: DoDto) : void {

        let context = this.contextService.getContext()

        this.httpService.post(callback.policy, context).subscribe(
        {next: (data:ElementDto) => {
            this.frontendJson.next(data)
        }})
    }

    uncheckedPost(serverRequest: ServerRequest) : void {

        this.httpClient.post<ElementDto>(this.backend_URI + "/backend", serverRequest).subscribe(
        //this.httpService.post(serverRequest.function).subscribe(
        {next: (data:ElementDto) => {
            this.frontendJson.next(data)
        }})
    }

    detectCreateMenuBar(element:ElementDto) {
        if (element.type == "menu_bar") {
            this.menuBar.next(element)
        } else {
            element.children.forEach(child => {
                this.detectCreateMenuBar(child)
            })
        }
    }

    getAllMessages(element:ElementDto, messageList:ElementDto[]) {

        if (element.type == "message") {
            messageList.push(element)
            console.log("HEYY")
            console.log(element)
        } else {
            element.children.forEach(child => {
                this.getAllMessages(child, messageList)
            })
        }

    }




}