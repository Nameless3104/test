package day06.service;

import day06.dao.UserDao;
import day06.dao.UserDaoImpl;
import day06.po.User;
import day06.utils.PageInfo;

import java.util.List;

public class UserServiceImpl implements UserService{

    private UserDao userDao = new UserDaoImpl();

    @Override
    public int addUser(User user) {
        return userDao.addUser(user);
    }

    @Override
    public int deleteUser(int id) {
        return userDao.deleteUser(id);
    }

    @Override
    public User findUserById(int id) {
        return userDao.findUserById(id);
    }

    @Override
    public boolean findUserByName(String name) {
        return userDao.findUserByName(name);
    }

    @Override
    public int updateUser(User user) {
        return userDao.updateUser(user);
    }

    @Override
    public List<User> queryAll() {
        return userDao.queryAll();
    }

    @Override
    public User login(String username, String password) {
        return userDao.login(username, password);
    }

    @Override
    public List<User> queryAllPage(PageInfo pageInfo, User user) {
        return userDao.queryAllPage(pageInfo, user);
    }

    @Override
    public int getTotalCount() {
        return userDao.getTotalCount();
    }

}
