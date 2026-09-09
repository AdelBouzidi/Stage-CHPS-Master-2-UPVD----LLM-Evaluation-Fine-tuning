program main
  implicit none
  integer :: lst_len
  integer, allocatable :: lst(:)
  integer :: result
  integer :: i

  ! Read input
  read(*,*) lst_len
  allocate(lst(lst_len))
  read(*,*) lst

  ! Calculate result - sum of odd elements at even positions (0-based indexing)
  result = 0
  do i = 0, lst_len - 1
    if (mod(i, 2) == 0 .and. mod(lst(i), 2) /= 0) then
      result = result + lst(i)
    end if
  end do

  ! Output result
  print *, result

end program main