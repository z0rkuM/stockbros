import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class LoginService {

  private loginUrl = 'http://91.117.52.106/StockBros/auth';

    constructor (private http: Http) { }

    doLogin(username: string, password: string): Promise<number> {
        const base64hash = 'Basic ' + btoa(username + ':' + password);
        const headers = new Headers();
        headers.append('Authorization', base64hash);
        return this.http.get(this.loginUrl, {headers: headers})
            .toPromise()
            .then(response => response.status as number);
    }

    logout() {
        localStorage.removeItem('b64Hash');
    }

}
