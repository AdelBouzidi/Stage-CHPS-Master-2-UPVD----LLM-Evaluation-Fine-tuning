program choose_num
  implicit none
  integer :: x, y, result

  ! Read input
  read *, x
  read *, y

  ! Call the function
  result = choose_num(x, y)

  ! Print output
  print *, result

contains

  function choose_num(x, y) result(res)
    implicit none
    integer, intent(in) :: x, y
    integer :: res

    if (x > y) then
      res = -1
    else
      res = y
      if (mod(res, 2) /= 0) then
        res = res - 1
      end if
      if (res < x) then
        res = -1
      end if
    end if
  end function choose_num

end program choose_num