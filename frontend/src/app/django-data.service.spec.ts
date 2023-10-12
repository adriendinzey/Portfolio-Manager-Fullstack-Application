import { TestBed } from '@angular/core/testing';

import { DjangoDataService } from './django-data.service';

describe('DjangoDataService', () => {
  let service: DjangoDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DjangoDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
