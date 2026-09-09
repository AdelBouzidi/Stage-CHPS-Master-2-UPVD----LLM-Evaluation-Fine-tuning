program main
  implicit none
  integer, parameter :: MAX_LEN = 100
  integer :: lst_len
  integer :: lst(MAX_LEN)
  integer :: result
  
  ! Read input
  read(*,*) lst_len
  read(*,*) (lst(i), i=1, lst_len)
  
  ! Calculate result
  result = 0
  do i = 1, lst_len
    if (mod(i, 2) == 0 .and. mod(lst(i), 2) == 1) then
      result = result + lst(i)
    end if
  end do
  
  ! Print output
  print *, result
end program main