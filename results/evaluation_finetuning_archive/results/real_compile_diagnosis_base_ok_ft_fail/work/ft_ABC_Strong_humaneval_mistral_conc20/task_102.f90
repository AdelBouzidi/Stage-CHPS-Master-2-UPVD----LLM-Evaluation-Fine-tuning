program choose_num_demo
  implicit none
  integer :: x, y, result

  ! Read input values
  read(*,*) x
  read(*,*) y

  ! Call the function
  result = choose_num(x, y)

  ! Output the result
  print(*,*) result

contains

  function choose_num(x, y) result(res)
    implicit none
    integer, intent(in) :: x, y
    integer :: res
    integer :: even_num

    if (x > y) then
      res = -1
      return
    end if

    ! Find the largest even number in [x, y]
    if (mod(y, 2) == 0) then
      even_num = y
    else
      even_num = y - 1
    end if

    if (even_num < x) then
      res = -1
    else
      res = even_num
    end if

  end function choose_num

end program choose_num_demo