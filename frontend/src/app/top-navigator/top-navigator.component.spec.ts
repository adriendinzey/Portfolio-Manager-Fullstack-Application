import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopnavigatorComponent } from './top-navigator.component';

describe('TopnavigatorComponent', () => {
  let component: TopnavigatorComponent;
  let fixture: ComponentFixture<TopnavigatorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TopnavigatorComponent]
    });
    fixture = TestBed.createComponent(TopnavigatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
