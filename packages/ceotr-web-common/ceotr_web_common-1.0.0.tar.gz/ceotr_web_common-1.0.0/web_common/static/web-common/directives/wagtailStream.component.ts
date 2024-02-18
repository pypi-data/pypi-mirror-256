import {Component, Input} from '@angular/core';

@Component({
  selector: 'wagtail-stream',
  templateUrl: './ng-wagtail-stream.html',
})

export class WagtailStreamComponent {

    @Input() blocks;

    constructor() {
    }
}
