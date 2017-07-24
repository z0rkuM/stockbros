import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { User } from '../class/user';
import { LoginService } from '../../service/login.service';
import { AlertService } from '../../service/alert.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  model: User = new User('', '');
  loading = false;
  returnUrl: string;

  constructor(
    private loginService: LoginService,
    private alertService: AlertService,
    private router: Router,
    private route: ActivatedRoute
  ){ }

  ngOnInit() {
    // reset login status
    this.loginService.logout();
    // get return url from route parameters or default to '/'
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
  }

  onSubmit() {
    this.loginService.doLogin(this.model.name, this.model.password).then(
      data => {
        const base64hash = btoa(this.model.name + ':' + this.model.password);
        localStorage.setItem('b64Hash', base64hash);
        this.router.navigate(['/stocks']);
      }
    ).catch(error => {
      this.alertService.error('El Usuario y/o contraseña no son correctos.');
      this.loading = false;
    });
  }
}
