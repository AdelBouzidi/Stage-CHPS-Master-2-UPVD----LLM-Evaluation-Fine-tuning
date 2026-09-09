program choose_num_demo
  implicit none
  integer :: x, y, result

  ! Read input
  read *, x
  read *, y

  ! Call the function
  result = choose_num(x, y)

  ! Output result
  print *, result

contains

  function choose_num(x, y) result(res)
    implicit none
    integer, intent(in) :: x, y
    integer :: res
    integer :: i

    ! Find the largest even number in range [x, y]
    do i = y, x, -1
      if (mod(i, 2) == 0) then
        res = i
        return
      end if
    end do

    res = -1
  end function choose_num

end program choose_num_demo