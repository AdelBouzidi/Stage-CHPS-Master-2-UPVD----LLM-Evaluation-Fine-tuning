program vowels_count
  implicit none
  character(len=100) :: input
  integer :: result

  ! Read input string
  read *, input

  ! Count vowels
  result = vowels_count(input)

  ! Output result
  print *, result

contains

  integer function vowels_count(s)
    character(len=*), intent(in) :: s
    integer :: i, len_s, count
    character(len=1) :: c

    len_s = len_trim(s)
    count = 0

    do i = 1, len_s
      c = s(i:i)
      select case (c)
      case ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
        count = count + 1
      case ('y', 'Y')
        if (i == len_s) then
          count = count + 1
        end if
      end select
    end do

    vowels_count = count
  end function vowels_count

end program vowels_count