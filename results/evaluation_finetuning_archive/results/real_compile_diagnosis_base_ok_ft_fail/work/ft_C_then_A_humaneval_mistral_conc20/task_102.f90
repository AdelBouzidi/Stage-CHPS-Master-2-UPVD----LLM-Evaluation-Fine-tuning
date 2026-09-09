program choose_num_demo
  implicit none
  integer :: x, y, result

  ! Read input from stdin
  read *, x
  read *, y

  result = choose_num(x, y)

  print *, result

contains

  integer function choose_num(x, y)
    implicit none
    integer, intent(in) :: x, y
    integer :: i

    ! Find the largest even number in the range [x, y]
    do i = y, x, -1
      if (mod(i, 2) == 0) then
        choose_num = i
        return
      end if
    end do

    choose_num = -1
  end function choose_num

end program choose_num_demo