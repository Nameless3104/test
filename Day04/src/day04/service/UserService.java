package day04.service;

import day04.po.User;

import java.util.List;

public interface UserService {
    List<User> queryAll(User aUser);

    User login(String username, String pwd);
}
