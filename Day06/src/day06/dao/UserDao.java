package day06.dao;

import day06.po.User;
import day06.utils.PageInfo;

import java.util.List;

public interface UserDao {

    int addUser(User user);

    int deleteUser(int id);

    User findUserById(int id);

    boolean findUserByName(String name);

    int updateUser(User user);

    List<User> queryAll();

    User login(String username, String password);

    List<User> queryAllPage(PageInfo pageInfo, User user);

    int getTotalCount();

}
