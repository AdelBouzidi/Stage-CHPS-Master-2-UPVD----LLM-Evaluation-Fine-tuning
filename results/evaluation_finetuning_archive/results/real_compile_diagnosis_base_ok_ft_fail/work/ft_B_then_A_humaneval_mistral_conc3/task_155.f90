program even_odd_count_demo
  implicit none
  type :: tuple
    integer :: first
    integer :: second
  end type tuple
  integer :: num
  type(tuple) :: res

  read(*, *) num
  res = even_odd_count(num)
  print *, res%first, res%second
end program even_odd_count_demo