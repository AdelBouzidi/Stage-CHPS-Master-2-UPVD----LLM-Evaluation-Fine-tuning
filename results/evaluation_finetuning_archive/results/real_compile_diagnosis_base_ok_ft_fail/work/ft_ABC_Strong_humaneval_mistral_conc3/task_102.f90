program choose_num_demo
  implicit none
  integer :: x, y, result

  ! Read input values
  read(*,*) x, y

  ! Call the function
  result = choose_num(x, y)

  ! Print the result
  print(*,*) result

contains

  integer function choose_num(x, y)
    integer, intent(in) :: x, y
    integer :: i

    ! Find the largest even number in range [x, y]
    do i = y, x, -1
      if (mod(i, 2) == 0) then
        choose_num = i
        return
      end if
    end do

    choose_num = -1
  end function choose_num

end program choose_num_demo