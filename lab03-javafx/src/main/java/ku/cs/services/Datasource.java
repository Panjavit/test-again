package ku.cs.services;

public interface Datasource<T> {
    T readData();  //T คือ Generic Type ใช้แทน Data type ของคลาสใดก็ได้
    void writeData(T data);
}