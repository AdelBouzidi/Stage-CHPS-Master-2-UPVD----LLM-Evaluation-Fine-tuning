program choose_num_demo
  implicit none
  integer :: x, y, result

  ! Read input from stdin
  read(*,*) x
  read(*,*) y

  ! Call the function
  result = choose_num(x, y)

  ! Print output to stdout
  print *, result

contains

  function choose_num(x, y) result(res)
    implicit none
    integer, intent(in) :: x, y
    integer :: res

    if (x > y) then
      res = -1
    else if (mod(y, 2) == 0) then
      res = y
    else
      res = y - 1
    end if

  end function choose_num

end program choose_num_demo