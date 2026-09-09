program main
  implicit none
  integer :: lst_len
  integer, allocatable :: lst(:)
  integer :: result

  ! Read input
  read(*,*) lst_len
  allocate(lst(lst_len))
  read(*,*) lst

  ! Calculate result
  result = 0
  do i = 1, lst_len
    if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) /= 0) then
      result = result + lst(i)
    end if
  end do

  ! Output result
  print *, result

end program main