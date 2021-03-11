package day04.service;

import day04.dao.UserDao;
import day04.dao.UserDaoImpl;
import day04.po.User;

import java.util.List;

public class UserServiceImpl implements UserService{

    @Override
    public List<User> queryAll(User aUser) {
        UserDao userDao = new UserDaoImpl();
        return userDao.queryAll(aUser);
    }

    @Override
    public User login(String username, String pwd) {
        User aUser = new User(username, pwd);
        return new UserDaoImpl().queryAUser(aUser);
    }
}
