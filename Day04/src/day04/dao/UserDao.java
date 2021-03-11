package day04.dao;

import day04.po.User;

import java.util.List;

public interface UserDao {
    List<User> queryAll(User aUser);
    User queryAUser(User aUser);
}
