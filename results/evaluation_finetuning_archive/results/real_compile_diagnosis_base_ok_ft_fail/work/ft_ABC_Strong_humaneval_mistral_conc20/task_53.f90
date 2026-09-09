program add_demo
  implicit none
  integer :: x, y, result

  ! Read input values
  read(*,*) x, y

  ! Calculate result
  result = add(x, y)

  ! Output result
  print(*,*) result

contains

  integer function add(x, y)
    integer, intent(in) :: x, y
    add = x + y
  end function add

end program add_demo