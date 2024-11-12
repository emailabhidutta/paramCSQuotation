import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../services/auth.service';

interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {
  userForm: FormGroup;
  users: User[] = [];
  errorMessage: string = '';
  successMessage: string = '';
  editingUser: User | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService
  ) {
    this.userForm = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      role: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    this.authService.getUsers().subscribe(
      (users: User[]) => {
        this.users = users;
        this.errorMessage = '';
      },
      error => {
        console.error('Error fetching users', error);
        this.errorMessage = 'Failed to load users. Please try again.';
      }
    );
  }

  onSubmit() {
    if (this.userForm.valid) {
      if (this.editingUser) {
        this.updateUser();
      } else {
        this.createUser();
      }
    } else {
      this.errorMessage = 'Please fill all required fields correctly.';
      this.successMessage = '';
    }
  }

  createUser() {
    this.authService.createUser(this.userForm.value).subscribe(
      response => {
        console.log('User created successfully', response);
        this.successMessage = 'User created successfully!';
        this.errorMessage = '';
        this.userForm.reset();
        this.loadUsers();
      },
      error => {
        console.error('Error creating user', error);
        this.errorMessage = 'Failed to create user. Please try again.';
        this.successMessage = '';
      }
    );
  }

  updateUser() {
    if (this.editingUser) {
      const updatedUser = { ...this.editingUser, ...this.userForm.value };
      this.authService.updateUser(updatedUser).subscribe(
        response => {
          console.log('User updated successfully', response);
          this.successMessage = 'User updated successfully!';
          this.errorMessage = '';
          this.userForm.reset();
          this.editingUser = null;
          this.loadUsers();
        },
        error => {
          console.error('Error updating user', error);
          this.errorMessage = 'Failed to update user. Please try again.';
          this.successMessage = '';
        }
      );
    }
  }

  editUser(user: User) {
    this.editingUser = user;
    this.userForm.patchValue({
      username: user.username,
      email: user.email,
      role: user.role
    });
    this.userForm.get('password')?.setValidators(null);
    this.userForm.get('password')?.updateValueAndValidity();
  }

  cancelEdit() {
    this.editingUser = null;
    this.userForm.reset();
    this.userForm.get('password')?.setValidators(Validators.required);
    this.userForm.get('password')?.updateValueAndValidity();
  }

  deleteUser(user: User) {
    if (confirm(`Are you sure you want to delete ${user.username}?`)) {
      this.authService.deleteUser(user.id).subscribe(
        () => {
          console.log('User deleted successfully');
          this.successMessage = 'User deleted successfully!';
          this.errorMessage = '';
          this.loadUsers();
        },
        error => {
          console.error('Error deleting user', error);
          this.errorMessage = 'Failed to delete user. Please try again.';
          this.successMessage = '';
        }
      );
    }
  }
}
