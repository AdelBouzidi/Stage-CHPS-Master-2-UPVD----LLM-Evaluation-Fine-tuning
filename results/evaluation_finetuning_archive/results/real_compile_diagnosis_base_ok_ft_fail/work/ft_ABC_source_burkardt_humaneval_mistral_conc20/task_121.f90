program solution
  implicit none
  integer :: lst_len
  integer, allocatable :: lst(:)
  integer :: result

  read(*,*) lst_len
  allocate(lst(lst_len))
  read(*,*) lst

  result = 0
  do i = 1, lst_len
    if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) == 1) then
      result = result + lst(i)
    end if
  end do

  print *, result

contains

  subroutine solution(lst_len, lst, result)
    integer, intent(in) :: lst_len
    integer, intent(in) :: lst(lst_len)
    integer, intent(out) :: result
    integer :: i

    result = 0
    do i = 1, lst_len
      if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) == 1) then
        result = result + lst(i)
      end if
    end do
  end subroutine solution

end program solution